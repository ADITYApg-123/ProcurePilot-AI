import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend")))

from app.schemas.quotation import VendorQuotation
from app.services.analysis_engine import analysis_engine

def generate_demo():
    ground_truth_path = os.path.join(os.path.dirname(__file__), "..", "..", "backend", "sample_data", "ground_truth.json")
    with open(ground_truth_path, "r") as f:
        data = json.load(f)
        
    quotations = [VendorQuotation(**q) for q in data]
    result = analysis_engine.analyze(quotations)
    
    out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "src", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "demoAnalysis.json")
    
    with open(out_path, "w") as f:
        f.write(result.model_dump_json(indent=2))
        
    print(f"Generated demo analysis at {out_path}")

if __name__ == "__main__":
    generate_demo()
