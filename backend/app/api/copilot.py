"""
Copilot API — Handles AI conversational capabilities.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.analysis import CopilotRequest, CopilotResponse
from app.services.job_manager import job_manager

router = APIRouter()


@router.post("/copilot/chat", response_model=CopilotResponse)
def copilot_chat(request: CopilotRequest):
    """
    Chat with the procurement copilot about a specific analysis job.
    """
    job = job_manager.get_job(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    # Stub response
    return CopilotResponse(
        response=f"I am the ProcurePilot. You asked: {request.message}",
        sources=["Vendor A", "Vendor B"]
    )
