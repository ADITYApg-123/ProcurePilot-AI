"""
Jobs API — Check the status of ongoing analysis.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.analysis import JobResponse, JobStatus
from app.services.job_manager import job_manager

router = APIRouter()


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_status(job_id: str):
    """
    Retrieve the current status of an analysis job.
    """
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobResponse(
        job_id=job.id,
        status=job.status,
        progress_message=job.progress_message,
        result=job.result if job.status == JobStatus.COMPLETED else None,
    )
