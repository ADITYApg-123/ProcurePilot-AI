"""
Document Extraction Service.
Uses Gemini 2.5 Flash to extract structured data from vendor quotations.
"""

import os
from google import genai
from google.genai import types
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
        You are an expert procurement analyst. Analyze this vendor quotation document.
        Extract all commercial and technical details accurately.
        If a field is missing in the document, leave it empty or null (do not guess).
        Pay special attention to the pricing, tax, warranty, and delivery terms.
        """

        retries = 0
        while retries < settings.MAX_EXTRACTION_RETRIES:
            try:
                response = client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=[uploaded_file, prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=VendorQuotation,
                        temperature=0.1,  # Low temperature for deterministic extraction
                    ),
                )
                
                # The response.text is guaranteed to match our Pydantic schema
                # We parse it directly into our Pydantic model
                quotation = VendorQuotation.model_validate_json(response.text)
                
                return ExtractionResult(
                    success=True,
                    quotation=quotation,
                    retries_used=retries,
                    source_file=pdf_path
                )
                
            except Exception as e:
                retries += 1
                print(f"Extraction attempt {retries} failed: {str(e)}")
                
        return ExtractionResult(
            success=False,
            error=f"Failed to extract valid data after {settings.MAX_EXTRACTION_RETRIES} attempts.",
            retries_used=retries,
            source_file=pdf_path
        )


# Singleton
extractor = DocumentExtractor()
