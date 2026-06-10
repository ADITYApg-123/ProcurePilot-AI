"""
Test the Document Extractor against a sample PDF.
"""

import sys
import os

# Add the backend directory to Python path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.services.extractor import extractor

def test_extraction():
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data", "Vendor_A_Apex.pdf")
    
    print(f"Testing extraction on: {pdf_path}")
    result = extractor.extract_quotation(pdf_path)
    
    if result.success:
        print("\n[SUCCESS] Extraction Successful!")
        print("\nExtracted Data:")
        print(result.quotation.model_dump_json(indent=2))
    else:
        print("\n[FAILED] Extraction Failed!")
        print(f"Error: {result.error}")

if __name__ == "__main__":
    test_extraction()
