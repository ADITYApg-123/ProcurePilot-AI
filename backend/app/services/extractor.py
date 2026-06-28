"""
Document Extraction Service.
Uses Gemini 2.5 Flash to extract structured data from vendor quotations.
"""

import os
from google import genai
from google.genai import types
from google.genai.errors import APIError
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from app.config import settings
from app.schemas.quotation import VendorQuotation, ExtractionResult

# Initialize the Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


class DocumentExtractor:
    """Handles vision extraction and structured validation."""

    def extract_quotation(self, pdf_path: str) -> ExtractionResult:
        """
        Extracts structured data from a PDF quotation using Gemini 2.5 Flash.
        Enforces output schema using Pydantic.
        """
        print(f"Extracting data from {pdf_path}...")
        
        # Upload the PDF to Gemini
        try:
            uploaded_file = client.files.upload(
                file=pdf_path,
                config={'mime_type': 'application/pdf'}
            )
            print(f"Uploaded file to Gemini: {uploaded_file.name}")
        except Exception as e:
            return ExtractionResult(
                success=False,
                error=f"Failed to upload PDF to Gemini: {str(e)}",
                source_file=pdf_path
            )

        prompt = """
        You are an expert procurement analyst AND a contract lawyer. Analyze this vendor quotation document carefully, including ALL pages — especially any Terms & Conditions, Payment Schedule, Penalty / Liquidated Damages, Warranty, Limitation of Liability, and Force Majeure sections.

        Extract ALL commercial and technical details accurately.
        If a field is missing in the document, leave it empty or null (do not guess).
        Pay special attention to the pricing, tax, warranty, and delivery terms.

        CRITICAL: Keep all extracted text fields (like special_conditions, warranty_terms, delivery_terms) extremely concise. Summarize them in 1-2 sentences. DO NOT copy-paste entire pages of terms and conditions into the JSON.

        CRITICAL: For every field you extract, you MUST provide a confidence score (0-100) in the `confidence_scores` dictionary. 100 means you found it explicitly in the text, 50 means it was ambiguous or inferred, 0 means missing.

        ALSO CRITICAL — extract the `contract_clauses` object with all 4 sub-fields:

        1. `payment_terms_days`: Read the FIRST payment milestone/tranche. Count how many calendar days after Purchase Order issuance the FIRST payment is due. If payment is required BEFORE or ON the same day as PO issuance (e.g. advance/mobilisation tranche), set this to 0. If Net 30 from delivery, set to ~30.

        2. `penalty_pct_per_week`: Find the Liquidated Damages (LD) or penalty clause. Calculate the effective % of total contract value per WEEK for the FIRST tier of delay:
           - If given as "X% per 3 calendar days" → weekly_rate = (X / 3) * 7
           - If given as "INR Y per calendar day" (flat daily amount) → weekly_rate = (Y * 7) / grand_total * 100
           - Use the rate AFTER any grace period. If no LD clause exists, return null.

        3. `liability_capped`: True if the vendor's aggregate liability is capped at a specific amount (e.g. 100% of PO value). True even if the cap can expand only in rare safety events. False only if there is NO cap at all.

        4. `force_majeure_included`: True if ANY force majeure clause is present (even if narrowly defined). False only if completely absent.
        """

        @retry(
            wait=wait_exponential(multiplier=2, min=4, max=60),
            stop=stop_after_attempt(settings.MAX_EXTRACTION_RETRIES),
            retry=retry_if_exception_type(APIError)
        )
        def _generate():
            return client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[uploaded_file, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=VendorQuotation,
                    temperature=0.1,
                    max_output_tokens=8192,
                ),
            )

        try:
            response = _generate()
            
            # Clean potential markdown wrapping from the response
            raw_json = response.text.strip()
            if raw_json.startswith("```json"):
                raw_json = raw_json[7:]
            if raw_json.startswith("```"):
                raw_json = raw_json[3:]
            if raw_json.endswith("```"):
                raw_json = raw_json[:-3]
            raw_json = raw_json.strip()
            
            quotation = VendorQuotation.model_validate_json(raw_json)
            
            return ExtractionResult(
                success=True,
                quotation=quotation,
                retries_used=0,
                source_file=pdf_path
            )
            
        except Exception as e:
            from tenacity import RetryError
            if isinstance(e, RetryError):
                inner_e = e.last_attempt.exception()
                error_msg = str(inner_e)
            else:
                error_msg = str(e)
                
            print(f"Extraction failed: {error_msg}")
            if hasattr(e, 'text'):
                print(f"Raw response was: {e.text}")
                
            return ExtractionResult(
                success=False,
                error=f"Extraction failed: {error_msg}",
                retries_used=settings.MAX_EXTRACTION_RETRIES,
                source_file=pdf_path
            )


# Singleton
extractor = DocumentExtractor()
