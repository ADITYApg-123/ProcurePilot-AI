"""
Test the Procurement Copilot Engine.
"""

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.schemas.quotation import VendorQuotation
from app.services.analysis_engine import analysis_engine
from app.services.copilot_engine import copilot_engine

def test_copilot():
    # 1. Load data and run deterministic analysis
    ground_truth_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data", "ground_truth.json")
    with open(ground_truth_path, "r") as f:
        data = json.load(f)
        
    quotations = [VendorQuotation(**q) for q in data]
    analysis = analysis_engine.analyze(quotations)
    
    print("=== TESTING COPILOT Q&A ===")
    question = "Why did you recommend Apex over Beta?"
    print(f"User: {question}")
    response = copilot_engine.chat(question, analysis)
    print(f"\nProcurePilot:\n{response.response}")
    print(f"Sources identified: {response.sources}\n")
    
    print("=== TESTING NEGOTIATION STRATEGY ===")
    target = "Beta Dynamics Engineering"
    print(f"Target Vendor: {target}")
    strategy = copilot_engine.generate_negotiation_strategy(target, analysis)
    print(f"\nStrategy:\n{strategy}")

if __name__ == "__main__":
    test_copilot()
