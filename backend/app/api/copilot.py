"""
Copilot API — Handles AI conversational capabilities.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.analysis import CopilotRequest, CopilotResponse, JobStatus, NegotiateRequest
from app.services.job_manager import job_manager
from app.services.copilot_engine import copilot_engine

router = APIRouter()


@router.post("/copilot/chat", response_model=CopilotResponse)
def copilot_chat(request: CopilotRequest):
    """
    Chat with the procurement copilot about a specific analysis job.
    """
    if request.analysis_context:
        analysis = request.analysis_context
    else:
        job = job_manager.get_job(request.job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
            
        try:
            from app.schemas.analysis import ProcurementAnalysis
            analysis = ProcurementAnalysis.model_validate(job.result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Invalid analysis data: {str(e)}")
        
    return copilot_engine.chat(request.message, analysis)

@router.post("/copilot/negotiate")
def generate_negotiation(request: NegotiateRequest):
    """
    Generate a negotiation strategy and email draft for a specific vendor.
    """
    if request.analysis_context:
        analysis = request.analysis_context
    else:
        job = job_manager.get_job(request.job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
            
        try:
            from app.schemas.analysis import ProcurementAnalysis
            analysis = ProcurementAnalysis.model_validate(job.result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Invalid analysis data: {str(e)}")
            
    strategy = copilot_engine.generate_negotiation_strategy(request.vendor_name, analysis)
    
    return {"vendor_name": request.vendor_name, "strategy": strategy}
