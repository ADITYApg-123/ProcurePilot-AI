"use client";

import React, { useState, useCallback, useRef } from 'react';
import { UploadCloud, File as FileIcon, X, CheckCircle, AlertCircle } from 'lucide-react';
import { Card } from './ui/Card';
import { Spinner } from './ui/Spinner';
import './UploadWorkspace.css';

interface UploadWorkspaceProps {
  onUpload: (files: File[]) => Promise<void>;
  onLoadDemo?: () => void;
  isUploading: boolean;
  error?: string | null;
}

export function UploadWorkspace({ onUpload, onLoadDemo, isUploading, error }: UploadWorkspaceProps) {
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

  return (
    <Card className="upload-workspace animate-fade-in">
      <div className="architecture-banner">
        <span className="banner-icon">⚙️</span>
        <div className="banner-content">
          <strong>Deterministic-First Architecture</strong>
          <p>✓ Financial math = Pure Python (zero AI) &nbsp;•&nbsp; ✓ AI = Data extraction only &nbsp;•&nbsp; ✓ No hallucinations in scores</p>
        </div>
      </div>

      <div className="upload-header">
        <h2>Procurement Workspace</h2>
        <p className="hero-tagline">Compare vendor quotes in seconds. Math, not hallucinations.</p>
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

      <div className="how-it-works animate-fade-in">
        <h4>How it Works</h4>
        <div className="pipeline-steps">
          <div className="step">
            <div className="step-number">1</div>
            <strong>Upload PDFs</strong>
            <span>Vendor quotes</span>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">2</div>
            <strong>AI Extracts</strong>
            <span>Structured data via Gemini Flash</span>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">3</div>
            <strong>Math Scores</strong>
            <span>Pure Python logic</span>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">4</div>
            <strong>Copilot Advises</strong>
            <span>Grounded reasoning</span>
          </div>
        </div>
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
