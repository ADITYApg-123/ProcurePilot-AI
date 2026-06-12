export interface VendorScore {
  vendor_name: string;
  cost_score: number;
  warranty_score: number;
  delivery_score: number;
  overall_score: number;
  rank: number;
}

export interface RiskFlag {
  vendor_name: string;
  risk_type: string;
  description: string;
  level: string;
}

export interface SavingsOpportunity {
  cheaper_vendor: string;
  expensive_vendor: string;
  savings_amount: number;
  savings_percentage: number;
}

export interface ProcurementAnalysis {
  vendor_scores: VendorScore[];
  recommended_vendor: string;
  recommendation_reason: string;
  risk_flags: RiskFlag[];

  savings_opportunities: SavingsOpportunity[];
  cost_comparison: Record<string, number>;
  warranty_comparison: Record<string, number>;
  delivery_comparison: Record<string, number>;
}

export interface JobResponse {
  job_id: string;
  status: 'PENDING' | 'EXTRACTING' | 'VALIDATING' | 'ANALYZING' | 'COMPLETED' | 'FAILED';
  progress_message: string;
  result?: ProcurementAnalysis;
}

export interface CopilotResponse {
  response: string;
  sources: string[];
}
