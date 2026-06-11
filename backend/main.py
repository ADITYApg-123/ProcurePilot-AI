"""
ProcurePilot AI — Backend Server
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import upload, analysis, copilot, jobs

app = FastAPI(
    title="ProcurePilot AI",
    description="Intelligent Procurement Decision & Negotiation Copilot API",
    version="0.1.0",
)

# CORS — allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for hackathon deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(jobs.router, prefix="/api", tags=["Jobs"])
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(copilot.router, prefix="/api", tags=["Copilot"])


@app.get("/")
def root():
    return {
        "project": "ProcurePilot AI",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
