import { JobResponse, CopilotResponse } from './types';

const API_BASE = 'http://localhost:8000/api';

export const apiClient = {
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

  async askCopilot(jobId: string, message: string): Promise<CopilotResponse> {
    const response = await fetch(`${API_BASE}/copilot/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ job_id: jobId, message }),
    });

    if (!response.ok) {
      throw new Error('Failed to ask copilot');
    }

    return response.json();
  },

  async generateNegotiationStrategy(jobId: string, vendorName: string): Promise<{ vendor_name: string; strategy: string }> {
    const response = await fetch(`${API_BASE}/copilot/negotiate/${jobId}/${encodeURIComponent(vendorName)}`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error('Failed to generate negotiation strategy');
    }

    return response.json();
  }
};
