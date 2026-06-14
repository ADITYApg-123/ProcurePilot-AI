"""
Analysis API — Retrieve deterministic procurement intelligence.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.analysis import ProcurementAnalysis, JobStatus
from app.services.job_manager import job_manager
from fastapi.responses import Response
from app.services.pdf_generator import generate_report

router = APIRouter()


@router.get("/analysis/{job_id}", response_model=ProcurementAnalysis)
def get_analysis_results(job_id: str):
    """
    Retrieve the completed procurement analysis results for a job.
    """
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Analysis not yet completed")
        
    if not job.result:
        raise HTTPException(status_code=500, detail="Analysis completed but no result found")

    # In a real implementation, we would parse job.result into ProcurementAnalysis
    return job.result

@router.get("/report/{job_id}")
def download_executive_report(job_id: str):
    """
    Generate and download a PDF executive report of the analysis.
    """
    job = job_manager.get_job(job_id)
    if not job or job.status != JobStatus.COMPLETED or not job.result:
        raise HTTPException(status_code=404, detail="Analysis not found or incomplete")

    analysis = ProcurementAnalysis.model_validate(job.result)
    pdf_bytes = generate_report(analysis)
    
    return Response(
        content=bytes(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=ProcurePilot_Report_{job_id}.pdf"
        }
    )

@router.post("/report/generate")
def generate_custom_report(analysis: ProcurementAnalysis):
    """
    Generate and download a PDF executive report from direct analysis data.
    """
    pdf_bytes = generate_report(analysis)
    
    return Response(
        content=bytes(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=ProcurePilot_Report_Demo.pdf"
        }
    )
