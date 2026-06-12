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
  const [isWarming, setIsWarming] = useState(false);

  // Health ping to wake up backend and detect cold start
  useEffect(() => {
    const pingHealth = async () => {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
          setIsWarming(true);
        }, 3000); // If it takes more than 3s, show warming UI
        
        await apiClient.pingHealth(controller.signal);
        
        clearTimeout(timeoutId);
        setIsWarming(false);
      } catch (err) {
        console.error("Health check failed", err);
      }
    };
    pingHealth();
  }, []);

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
      setJobStatus({ job_id: res.job_id, status: 'PENDING', progress_message: 'Job created...' });
    } catch (err: any) {
      setUploadError(err.message || 'Failed to upload files.');
    }
  };

  const handleLoadDemo = async () => {
    try {
      // Need to type assert or handle default import correctly
      const demoData = (await import('../data/demoAnalysis.json')) as any;
      setJobId('demo-job-123');
      setAnalysis(demoData.default || demoData);
    } catch (err) {
      console.error('Failed to load demo data', err);
      setUploadError('Failed to load demo data.');
    }
  };

  return (
    <main className="app-main">
      <header className="app-header">
        <div className="logo-container">
          <div className="logo-mark"></div>
          <h1>ProcurePilot</h1>
        </div>
        {isWarming && !jobId && (
          <div className="global-status warming-status">
            <span className="status-dot"></span>
            Waking up analysis engine... (may take up to 60s)
          </div>
        )}
        {jobStatus && jobStatus.status !== 'COMPLETED' && jobStatus.status !== 'FAILED' && (
          <div className="global-status">
            <span className="status-dot"></span>
            {jobStatus.progress_message}
          </div>
        )}
      </header>

      <div className="content-wrapper">
        {!analysis ? (
          <UploadWorkspace 
            onUpload={handleUpload} 
            onLoadDemo={handleLoadDemo}
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
