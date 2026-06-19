"use client";

import React, { useState, useCallback, useRef } from 'react';
import { UploadCloud, File as FileIcon, X, CheckCircle, AlertCircle } from 'lucide-react';
import { Card } from './ui/Card';
import { Spinner } from './ui/Spinner';
import { JobResponse } from '../services/types';
import './UploadWorkspace.css';

interface UploadWorkspaceProps {
  onUpload: (files: File[]) => Promise<void>;
  onLoadDemo?: () => void;
  isUploading: boolean;
  jobStatus?: JobResponse | null;
  error?: string | null;
}

export function UploadWorkspace({ onUpload, onLoadDemo, isUploading, jobStatus, error }: UploadWorkspaceProps) {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const files = Array.from(e.dataTransfer.files).filter(f => f.type === 'application/pdf');
      setSelectedFiles(prev => [...prev, ...files]);
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const files = Array.from(e.target.files).filter(f => f.type === 'application/pdf');
      setSelectedFiles(prev => [...prev, ...files]);
    }
  };

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUploadClick = () => {
    if (selectedFiles.length > 0) {
      onUpload(selectedFiles);
    }
  };

  if (jobStatus && jobStatus.status !== 'FAILED') {
    return (
      <Card className="upload-workspace animate-fade-in pipeline-view">
        <div className="pipeline-header">
          <h2>Analyzing Vendor Quotations</h2>
          <p className="hero-tagline">Deterministic extraction and math engine running...</p>
        </div>
        
        <div className="pipeline-stages">
          <div className={`pipeline-stage ${['UPLOADED', 'EXTRACTING', 'ANALYZING', 'COMPLETED'].includes(jobStatus.status) ? 'active' : ''}`}>
            <span className="stage-icon">📄</span>
            <span>Upload</span>
          </div>
          <div className="pipeline-connector"></div>
          <div className={`pipeline-stage ${['EXTRACTING', 'ANALYZING', 'COMPLETED'].includes(jobStatus.status) ? 'active' : ''}`}>
            <span className="stage-icon">🤖</span>
            <span>AI Extract</span>
          </div>
          <div className="pipeline-connector"></div>
          <div className={`pipeline-stage ${['ANALYZING', 'COMPLETED'].includes(jobStatus.status) ? 'active' : ''}`}>
            <span className="stage-icon">🧮</span>
            <span>Math Score</span>
          </div>
          <div className="pipeline-connector"></div>
          <div className={`pipeline-stage ${['COMPLETED'].includes(jobStatus.status) ? 'active' : ''}`}>
            <span className="stage-icon">💬</span>
            <span>Copilot</span>
          </div>
        </div>

        <div className="terminal-container">
          <div className="terminal-header">
            <span>🤖 AI EXTRACTION & SCORING LOG (Live)</span>
            {jobStatus.status === 'COMPLETED' ? <span className="status-badge success">Complete</span> : <span className="status-badge blinking">Processing...</span>}
          </div>
          <div className="terminal-body" ref={(el) => {
            if (el) el.scrollTop = el.scrollHeight;
          }}>
            {jobStatus.logs?.map((log, i) => (
              <div key={i} className="terminal-log-line">
                {log}
              </div>
            ))}
            {jobStatus.status !== 'COMPLETED' && (
              <div className="terminal-log-line blinking-cursor">_</div>
            )}
          </div>
        </div>
        <div className="deterministic-notice">
          <span className="gear-icon">⚙️</span> This pipeline is deterministic-first: AI handles extraction → Math handles scoring → No hallucinated numbers in your final vendor comparison.
        </div>
      </Card>
    );
  }

  return (
    <Card className="upload-workspace animate-fade-in">


      <div className="upload-header">
        <h2>100% Deterministic Procurement</h2>
        <p className="hero-tagline">Analyze vendor quotes with auditable financial math. Zero AI calculation hallucinations.</p>
      </div>

      {onLoadDemo && (
        <div className="demo-section animate-fade-in">
          <button className="btn-demo" onClick={onLoadDemo} disabled={isUploading}>
            <span className="fire-icon">🔥</span> Try Instant Demo (Load Pre-analyzed Sample Data)
          </button>
          <div className="demo-divider">
            <span>OR UPLOAD YOUR OWN PDFs</span>
          </div>
        </div>
      )}

      <div 
        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <UploadCloud className="upload-icon" size={48} />
        <h3>Drag & Drop Quotations Here</h3>
        <p>or click to browse from your computer</p>
        <input 
          type="file" 
          multiple 
          accept=".pdf" 
          ref={fileInputRef} 
          onChange={handleFileSelect} 
          style={{ display: 'none' }} 
        />
      </div>



      {error && (
        <div className="upload-error">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {selectedFiles.length > 0 && (
        <div className="file-list-container">
          <h4>Selected Files ({selectedFiles.length})</h4>
          <ul className="file-list">
            {selectedFiles.map((file, i) => (
              <li key={i} className="file-item animate-fade-in">
                <div className="file-info">
                  <FileIcon size={20} className="file-icon-small" />
                  <span className="file-name">{file.name}</span>
                </div>
                {!isUploading && (
                  <button className="remove-btn" onClick={() => removeFile(i)}>
                    <X size={18} />
                  </button>
                )}
                {isUploading && <CheckCircle size={18} className="success-icon" />}
              </li>
            ))}
          </ul>
          
          <button 
            className="btn-primary upload-btn" 
            onClick={handleUploadClick}
            disabled={isUploading}
          >
            {isUploading ? (
              <>
                <Spinner size={18} />
                Extracting Data...
              </>
            ) : (
              'Analyze Quotations'
            )}
          </button>
        </div>
      )}
    </Card>
  );
}
