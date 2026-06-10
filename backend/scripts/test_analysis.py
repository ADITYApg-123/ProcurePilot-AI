"""
Test the Deterministic Analysis Engine using the Ground Truth JSON data.
"""

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.schemas.quotation import VendorQuotation
from app.services.analysis_engine import analysis_engine

def test_analysis():
    ground_truth_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data", "ground_truth.json")
    
    with open(ground_truth_path, "r") as f:
        data = json.load(f)
        
    quotations = [VendorQuotation(**q) for q in data]
    
    print("Running Deterministic Analysis Engine...\n")
    result = analysis_engine.analyze(quotations)
    
    print("=== RECOMMENDED VENDOR ===")
    print(f"Vendor: {result.recommended_vendor}")
    print(f"Reason: {result.recommendation_reason}\n")
    
    print("=== VENDOR SCORES ===")
    for score in result.vendor_scores:
        print(f"{score.rank}. {score.vendor_name} - Overall: {score.overall_score} (Cost: {score.cost_score}, Warranty: {score.warranty_score}, Delivery: {score.delivery_score})")
        
    print("\n=== DETECTED RISKS ===")
    for risk in result.risk_flags:
        print(f"[{risk.level}] {risk.vendor_name}: {risk.description}")
        
    print("\n=== SAVINGS OPPORTUNITIES ===")
    for savings in result.savings_opportunities:
        print(f"Choosing {savings.cheaper_vendor} over {savings.expensive_vendor} saves ₹{savings.savings_amount:,.2f} ({savings.savings_percentage}%).")

if __name__ == "__main__":
    test_analysis()
