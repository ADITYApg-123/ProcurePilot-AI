export interface VendorScore {
  vendor_name: string;
  cost_score: number;
  warranty_score: number;
  delivery_score: number;
  overall_score: number;
  rank: number;
}

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH';

export interface ClauseRisk {
  extracted_value: string;
  risk_level: RiskLevel;
  note?: string;
}

export interface VendorClauseAnalysis {
  payment_terms: ClauseRisk;
  penalty: ClauseRisk;
  liability: ClauseRisk;
  force_majeure: ClauseRisk;
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
  confidence_scores: Record<string, Record<string, number>>;
  contract_analysis?: Record<string, VendorClauseAnalysis>;
}

export interface JobResponse {
  job_id: string;
  status: 'UPLOADED' | 'EXTRACTING' | 'VALIDATING' | 'ANALYZING' | 'GENERATING_RECOMMENDATION' | 'COMPLETED' | 'FAILED' | 'PENDING';
  progress_message: string;
  logs?: string[];
  result?: ProcurementAnalysis;
}

export interface CopilotResponse {
  response: string;
  sources: string[];
}
