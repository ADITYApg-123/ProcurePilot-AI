"""
Procurement Copilot Engine.
Uses Gemini to provide conversational intelligence, negotiation strategies,
and grounded reasoning on top of the deterministic analysis data.
"""

import json
from google import genai
from google.genai import types
from google.genai.errors import APIError
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from app.config import settings
from app.schemas.analysis import ProcurementAnalysis, CopilotResponse

client = genai.Client(api_key=settings.GEMINI_API_KEY)

class CopilotEngine:
    def chat(self, user_message: str, analysis: ProcurementAnalysis) -> CopilotResponse:
        """
        Handle a general Q&A chat message grounded in the analysis data.
        """
        # Provide the FULL analysis object to the Copilot so it can see raw costs and warranties
        context_data = analysis.model_dump()
        
        system_prompt = f"""
        You are ProcurePilot, an expert AI procurement copilot.
        Your job is to answer user questions about a recent procurement analysis.
        Use ONLY the following deterministic analysis data to answer. Do not hallucinate or guess.
        Be professional, concise, and analytical.
        
        METHODOLOGY (How the data was analyzed):
        1. AI Vision Extraction: The AI (Gemini) was strictly used ONLY to extract raw fields (Pricing, Warranty, Lead Times, Legal Clauses) directly from the uploaded vendor PDFs into strict JSON.
        2. Deterministic Math Engine: The AI does NOT calculate scores, rankings, or winners. All mathematical scoring and vendor comparison is done by a deterministic, hard-coded Python Math Engine to eliminate AI hallucinations.
        
        SCORING METHODOLOGY (The Exact Math Used):
        The overall score (0-100) is a weighted average of three normalized sub-scores:
        - Cost Score: 100 * (max_cost - vendor_cost) / (max_cost - min_cost)  [Lower cost gets higher score]
        - Warranty Score: 100 * (vendor_warranty - min_warranty) / (max_warranty - min_warranty)  [Longer warranty gets higher score]
        - Delivery Score: 100 * (max_delivery - vendor_delivery) / (max_delivery - min_delivery)  [Faster delivery gets higher score]
        - Risk Flags are triggered if: Warranty < 12 months, Delivery > 30 days, or 100% advance payment required.
        
        If the user asks how the data was analyzed, scored, or "what was the math", proudly explain this exact methodology and use the raw numbers from the context to walk them through the math.
        
        ANALYSIS CONTEXT:
        {json.dumps(context_data, indent=2)}
        """
        
        @retry(
            wait=wait_exponential(multiplier=1, min=2, max=10),
            stop=stop_after_attempt(3),
            retry=retry_if_exception_type(APIError)
        )
        def _generate_chat():
            return client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[user_message],
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3,
                )
            )

        try:
            response = _generate_chat()
            
            # Identify sources based on which vendors are mentioned in the response
            sources = []
            for score in analysis.vendor_scores:
                if score.vendor_name.lower() in response.text.lower():
                    sources.append(score.vendor_name)
                    
            return CopilotResponse(
                response=response.text,
                sources=sources
            )
        except Exception as e:
            return CopilotResponse(
                response=f"I encountered an error while analyzing the data: {str(e)}",
                sources=[]
            )

    def generate_negotiation_strategy(self, vendor_name: str, analysis: ProcurementAnalysis) -> str:
        """
        Generate a specific negotiation strategy for a given vendor.
        """
        context_data = {
            "target_vendor": vendor_name,
            "vendor_scores": [s.model_dump() for s in analysis.vendor_scores],
            "risk_flags": [r.model_dump() for r in analysis.risk_flags if r.vendor_name == vendor_name],
        }
        
        prompt = f"""
        You are an expert procurement negotiator.
        Generate a negotiation strategy to get a better deal from the target vendor.
        
        ANALYSIS CONTEXT:
        {json.dumps(context_data, indent=2)}
        
        Format your response nicely with:
        1. Leverage Points (What can we use against them? E.g., competitors are cheaper/faster)
        2. Key Asks (What should we request? E.g., extended warranty, price match)
        3. Email Draft (A professional email to the vendor)
        """
        
        @retry(
            wait=wait_exponential(multiplier=1, min=2, max=10),
            stop=stop_after_attempt(3),
            retry=retry_if_exception_type(APIError)
        )
        def _generate_strategy():
            return client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    temperature=0.5, # Slightly more creative for email drafting
                )
            )

        try:
            response = _generate_strategy()
            return response.text
        except Exception as e:
            return f"Failed to generate negotiation strategy: {str(e)}"

copilot_engine = CopilotEngine()
