"use client";

import React, { useState, useEffect } from 'react';
import { UploadWorkspace } from '../components/UploadWorkspace';
import { AnalysisDashboard } from '../components/AnalysisDashboard';
import { CopilotChat } from '../components/CopilotChat';
import { apiClient } from '../services/apiClient';
import { JobResponse, ProcurementAnalysis } from '../services/types';
import './page.css';

export default function Home() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<JobResponse | null>(null);
  const [analysis, setAnalysis] = useState<ProcurementAnalysis | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  // Poll for job status
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (jobId && jobStatus?.status !== 'COMPLETED' && jobStatus?.status !== 'FAILED') {
      interval = setInterval(async () => {
        try {
          const res = await apiClient.getJobStatus(jobId);
          setJobStatus(res);
          if (res.status === 'COMPLETED' && res.result) {
            setAnalysis(res.result);
            clearInterval(interval);
          } else if (res.status === 'FAILED') {
            setUploadError(res.progress_message || 'Extraction failed.');
            clearInterval(interval);
          }
        } catch (err) {
          console.error(err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [jobId, jobStatus?.status]);

  const handleUpload = async (files: File[]) => {
    setUploadError(null);
    try {
      const res = await apiClient.uploadFiles(files);
      setJobId(res.job_id);
      setJobStatus({ job_id: res.job_id, status: 'PENDING', message: 'Job created...' });
    } catch (err: any) {
      setUploadError(err.message || 'Failed to upload files.');
    }
  };

  return (
    <main className="app-main">
      <header className="app-header">
        <div className="logo-container">
          <div className="logo-mark"></div>
          <h1>ProcurePilot</h1>
        </div>
        {jobStatus && jobStatus.status !== 'COMPLETED' && jobStatus.status !== 'FAILED' && (
          <div className="global-status">
            <span className="status-dot"></span>
            {jobStatus.message}
          </div>
        )}
      </header>

      <div className="content-wrapper">
        {!analysis ? (
          <UploadWorkspace 
            onUpload={handleUpload} 
            isUploading={!!jobId && jobStatus?.status !== 'FAILED'} 
            error={uploadError} 
          />
        ) : (
          <div className="results-view animate-fade-in">
            <div className="main-content">
              <AnalysisDashboard jobId={jobId!} analysis={analysis} />
            </div>
            <div className="sidebar-content">
              <CopilotChat jobId={jobId!} analysis={analysis} />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
