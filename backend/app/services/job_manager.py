"""
Job Management Service.
Handles tracking and state of long-running analysis jobs.
"""

from typing import Dict, Optional, List
from pydantic import BaseModel
from app.schemas.analysis import JobStatus
import asyncio
from app.services.extractor import extractor
from app.services.analysis_engine import analysis_engine


class Job(BaseModel):
    id: str
    status: JobStatus
    progress_message: str
    file_paths: List[str]
    result: Optional[dict] = None


class JobManager:
    """
    In-memory job manager for the MVP.
    In a production system, this would use Redis/Celery + Database.
    """
    def __init__(self):
        self._jobs: Dict[str, Job] = {}

    def create_job(self, job_id: str, file_paths: List[str]) -> Job:
        job = Job(
            id=job_id,
            status=JobStatus.UPLOADED,
            progress_message="Documents uploaded successfully.",
            file_paths=file_paths
        )
        self._jobs[job_id] = job
        
        # Fire and forget background processing
        # In MVP we use asyncio.create_task instead of Celery
        asyncio.create_task(self._process_job(job_id))
        
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        return self._jobs.get(job_id)

    def update_job(self, job_id: str, status: JobStatus, message: str, result: Optional[dict] = None):
        if job_id in self._jobs:
            self._jobs[job_id].status = status
            self._jobs[job_id].progress_message = message
            if result:
                self._jobs[job_id].result = result

    async def _process_job(self, job_id: str):
        """
        Background processing pipeline placeholder.
        """
        # We will implement the actual pipeline here later:
        # 1. Extract (Vision AI)
        # 2. Validate (Pydantic)
        # 3. Analyze (Deterministic)
        
        self.update_job(job_id, JobStatus.EXTRACTING, "Extracting data from PDFs...")
        
        quotations = []
        for path in self._jobs[job_id].file_paths:
            result = extractor.extract_quotation(path)
            if not result.success:
                self.update_job(job_id, JobStatus.FAILED, f"Failed to extract {path}: {result.error}")
                return
            quotations.append(result.quotation)
            
        self.update_job(job_id, JobStatus.ANALYZING, "Running deterministic analysis...")
        
        try:
            analysis_result = analysis_engine.analyze(quotations)
            self.update_job(
                job_id, 
                JobStatus.COMPLETED, 
                "Analysis complete.", 
                result=analysis_result.model_dump()
            )
        except Exception as e:
            self.update_job(job_id, JobStatus.FAILED, f"Analysis failed: {str(e)}")

# Global singleton
job_manager = JobManager()
