"""
Copilot API — Handles AI conversational capabilities.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.analysis import CopilotRequest, CopilotResponse, JobStatus
from app.services.job_manager import job_manager
from app.services.copilot_engine import copilot_engine

router = APIRouter()


@router.post("/copilot/chat", response_model=CopilotResponse)
def copilot_chat(request: CopilotRequest):
    """
    Chat with the procurement copilot about a specific analysis job.
    """
    job = job_manager.get_job(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    # Convert the result dict back into a ProcurementAnalysis object
    # In a real app with DB, we'd fetch the structured object
    try:
        from app.schemas.analysis import ProcurementAnalysis
        analysis = ProcurementAnalysis.model_validate(job.result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid analysis data: {str(e)}")
        
    return copilot_engine.chat(request.message, analysis)

@router.post("/copilot/negotiate/{job_id}/{vendor_name}")
def generate_negotiation(job_id: str, vendor_name: str):
    """
    Generate a negotiation strategy and email draft for a specific vendor.
    """
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    try:
        from app.schemas.analysis import ProcurementAnalysis
        analysis = ProcurementAnalysis.model_validate(job.result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid analysis data: {str(e)}")
        
    strategy = copilot_engine.generate_negotiation_strategy(vendor_name, analysis)
    
    return {"vendor_name": vendor_name, "strategy": strategy}
