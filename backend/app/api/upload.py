"""
Upload API — Receives vendor quotation PDFs.
"""

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import settings
from app.schemas.analysis import JobStatus, JobResponse
from app.services.job_manager import job_manager

router = APIRouter()


@router.post("/upload", response_model=JobResponse)
async def upload_quotations(files: list[UploadFile] = File(...)):
    """
    Upload vendor quotation PDFs.
    Returns a job_id to track the analysis progress.
    """
    # Validate files
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Please upload at least 2 vendor quotations.")
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 quotations allowed.")

    saved_paths = []

    for file in files:
        # Validate extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.filename}. Only PDF files are allowed.",
            )

        # Validate size
        content = await file.read()
        size_mb = len(content) / (1024 * 1024)
        if size_mb > settings.MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} exceeds {settings.MAX_FILE_SIZE_MB}MB limit.",
            )

        # Save file
        job_id = str(uuid.uuid4())
        file_dir = os.path.join(settings.UPLOAD_DIR, job_id)
        os.makedirs(file_dir, exist_ok=True)

        file_path = os.path.join(file_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
        saved_paths.append(file_path)

    # Create job
    job_id = str(uuid.uuid4())
    job_manager.create_job(job_id, saved_paths)

    return JobResponse(
        job_id=job_id,
        status=JobStatus.UPLOADED,
        progress_message=f"Uploaded {len(files)} quotations. Analysis starting...",
    )
