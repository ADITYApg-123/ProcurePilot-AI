import { JobResponse, CopilotResponse, ProcurementAnalysis } from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const apiClient = {
  async pingHealth(signal?: AbortSignal): Promise<void> {
    const baseUrl = API_BASE.replace(/\/api$/, '');
    await fetch(`${baseUrl}/health`, { signal });
  },

  async uploadFiles(files: File[]): Promise<{ job_id: string; message: string }> {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));

    const response = await fetch(`${API_BASE}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload files');
    }

    return response.json();
  },

  async getJobStatus(jobId: string): Promise<JobResponse> {
    const response = await fetch(`${API_BASE}/jobs/${jobId}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch job status');
    }

    return response.json();
  },

  async askCopilot(jobId: string, message: string, analysis?: ProcurementAnalysis): Promise<CopilotResponse> {
    const body: any = { job_id: jobId, message };
    if (analysis) body.analysis_context = analysis;
    
    const response = await fetch(`${API_BASE}/copilot/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error('Failed to ask copilot');
    }

    return response.json();
  },

  async generateNegotiationStrategy(jobId: string, vendorName: string, analysis?: ProcurementAnalysis): Promise<{ vendor_name: string; strategy: string }> {
    const body: any = { job_id: jobId, vendor_name: vendorName };
    if (analysis) body.analysis_context = analysis;
    
    const response = await fetch(`${API_BASE}/copilot/negotiate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error('Failed to generate negotiation strategy');
    }

    return response.json();
  },

  async downloadReport(jobId: string): Promise<void> {
    const response = await fetch(`${API_BASE}/report/${jobId}`);
    
    if (!response.ok) {
      throw new Error('Failed to download report');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ProcurePilot_Report_${jobId}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }
};
