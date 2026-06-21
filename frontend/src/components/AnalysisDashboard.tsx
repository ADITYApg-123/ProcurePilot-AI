"use client";

import React from 'react';
import { Trophy, AlertTriangle, TrendingDown, DollarSign, Clock, ShieldCheck, Download, Zap, ShieldAlert, CheckCircle, FileText } from 'lucide-react';
import { ProcurementAnalysis, RiskFlag, VendorClauseAnalysis, ClauseRisk, RiskLevel } from '../services/types';
import { Card } from './ui/Card';
import { Badge } from './ui/Badge';
import { ConfidenceBar } from './ui/ConfidenceBar';
import { apiClient } from '../services/apiClient';
import { recalculateScores } from '../utils/scoring';
import { Sliders } from 'lucide-react';
import './AnalysisDashboard.css';

interface Props {
  jobId: string;
  analysis: ProcurementAnalysis;
}

export function AnalysisDashboard({ jobId, analysis }: Props) {
  const [isDownloading, setIsDownloading] = React.useState(false);

  // What-If Scenario Engine State
  const [costWeight, setCostWeight] = React.useState(50);
  const [warrantyWeight, setWarrantyWeight] = React.useState(20);
  const [deliveryWeight, setDeliveryWeight] = React.useState(30);
  const [displayAnalysis, setDisplayAnalysis] = React.useState(analysis);

  React.useEffect(() => {
    // Recalculate scores whenever sliders change
    const newAnalysis = recalculateScores(
      analysis,
      costWeight,
      warrantyWeight,
      deliveryWeight
    );
    setDisplayAnalysis(newAnalysis);
  }, [analysis, costWeight, warrantyWeight, deliveryWeight]);

  const handleDownload = async () => {
    try {
      setIsDownloading(true);
      await apiClient.downloadReport(jobId, analysis);
    } catch (err) {
      console.error(err);
      alert('Failed to download report.');
    } finally {
      setIsDownloading(false);
    }
  };
  const getBadgeVariant = (level: string) => {
    switch (level) {
      case 'HIGH': return 'error';
      case 'MEDIUM': return 'warning';
      default: return 'info';
    }
  };

  // Compute Insights
  const hasHighRisk = displayAnalysis.risk_flags.some(r => r.level === 'HIGH');
  const hasMedRisk = displayAnalysis.risk_flags.some(r => r.level === 'MEDIUM');
  const overallRisk = hasHighRisk ? 'HIGH' : hasMedRisk ? 'MEDIUM' : 'LOW';
  
  const maxSavings = displayAnalysis.savings_opportunities.length > 0 
    ? Math.max(...displayAnalysis.savings_opportunities.map(s => s.savings_amount))
    : 0;

  return (
    <div className="dashboard-container animate-fade-in">
      
      {/* Recommended Vendor Hero */}
      <Card className="hero-card tour-step-winner">
        <div className="hero-content">
          <div className="hero-icon">
            <Trophy size={48} />
          </div>
          <div className="hero-text">
            <h2>Recommended: {displayAnalysis.recommended_vendor}</h2>
            <p>{displayAnalysis.recommendation_reason}</p>
          </div>
        </div>
        <button 
          className="btn-primary" 
          style={{ marginTop: '20px' }}
          onClick={handleDownload}
          disabled={isDownloading}
        >
          <Download size={18} />
          {isDownloading ? 'Generating...' : 'Download Executive PDF Report'}
        </button>
      </Card>

      {/* What-If Scenario Engine */}
      <Card className="scenario-engine-card tour-step-sliders">
        <div className="scenario-header">
          <Sliders size={24} className="text-accent" />
          <div>
            <h3>⚡ What-If Scenario Engine</h3>
            <p>Adjust priorities and watch vendor rankings recalculate in real-time. Zero AI — pure deterministic math.</p>
          </div>
        </div>
        
        <div className="sliders-container">
          <div className="slider-group">
            <div className="slider-label">
              <span>Cost Priority</span>
              <span>{costWeight}%</span>
            </div>
            <input 
              type="range" 
              min="0" max="100" 
              value={costWeight} 
              onChange={(e) => setCostWeight(Number(e.target.value))}
              className="scenario-slider"
            />
          </div>
          
          <div className="slider-group">
            <div className="slider-label">
              <span>Warranty Priority</span>
              <span>{warrantyWeight}%</span>
            </div>
            <input 
              type="range" 
              min="0" max="100" 
              value={warrantyWeight} 
              onChange={(e) => setWarrantyWeight(Number(e.target.value))}
              className="scenario-slider"
            />
          </div>
          
          <div className="slider-group">
            <div className="slider-label">
              <span>Delivery Priority</span>
              <span>{deliveryWeight}%</span>
            </div>
            <input 
              type="range" 
              min="0" max="100" 
              value={deliveryWeight} 
              onChange={(e) => setDeliveryWeight(Number(e.target.value))}
              className="scenario-slider"
            />
          </div>
        </div>
      </Card>

      {/* Insights Row */}
      <div className="insights-row animate-fade-in tour-step-badges">
        <Card className="insight-card">
          <div className="insight-icon bg-success-light">
            <TrendingDown size={24} className="text-success" />
          </div>
          <div>
            <p className="insight-label">Potential Savings</p>
            <h4 className="insight-value">{maxSavings > 0 ? `₹${maxSavings.toLocaleString()}` : 'Optimized'}</h4>
          </div>
        </Card>
        
        <Card className="insight-card">
          <div className={`insight-icon ${overallRisk === 'HIGH' ? 'bg-error-light' : overallRisk === 'MEDIUM' ? 'bg-warning-light' : 'bg-success-light'}`}>
            <ShieldAlert size={24} className={overallRisk === 'HIGH' ? 'text-error' : overallRisk === 'MEDIUM' ? 'text-warning' : 'text-success'} />
          </div>
          <div>
            <p className="insight-label">Overall Risk Profile</p>
            <h4 className="insight-value">{overallRisk}</h4>
          </div>
        </Card>

        <Card className="insight-card">
          <div className="insight-icon bg-info-light">
            <CheckCircle size={24} className="text-accent" />
          </div>
          <div>
            <p className="insight-label">Math Confidence</p>
            <h4 className="insight-value">100% Deterministic</h4>
          </div>
        </Card>
      </div>

      <div className="dashboard-grid">
        {/* Standardized Vendor Comparison Table */}
        <div className="rankings-section">
          <h3>Vendor Comparison Matrix</h3>
          <Card className="table-card tour-step-matrix">
            <div className="table-responsive">
              <table className="comparison-table">
                <thead>
                  <tr>
                    <th>Metric</th>
                    {displayAnalysis.vendor_scores.map(score => (
                      <th key={score.vendor_name} className={score.vendor_name === displayAnalysis.recommended_vendor ? 'highlight-col' : ''}>
                        {score.vendor_name}
                        {score.vendor_name === displayAnalysis.recommended_vendor && (
                          <Badge variant="success" className="winner-badge">Winner</Badge>
                        )}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Overall Score</strong></td>
                    {displayAnalysis.vendor_scores.map(score => (
                      <td key={score.vendor_name} className={score.vendor_name === displayAnalysis.recommended_vendor ? 'highlight-col' : ''}>
                        <div className="score-circle">{score.overall_score.toFixed(1)}</div>
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td><strong>Total Cost</strong></td>
                    {displayAnalysis.vendor_scores.map(score => {
                      const costConf = displayAnalysis.confidence_scores?.[score.vendor_name]?.grand_total ?? 100;
                      return (
                        <td key={score.vendor_name} className={score.vendor_name === displayAnalysis.recommended_vendor ? 'highlight-col tour-step-confidence' : ''}>
                          ₹{displayAnalysis.cost_comparison[score.vendor_name].toLocaleString()}
                          <ConfidenceBar score={costConf} />
                        </td>
                      );
                    })}
                  </tr>
                  <tr>
                    <td><strong>Warranty</strong></td>
                    {displayAnalysis.vendor_scores.map(score => {
                      const warrantyConf = displayAnalysis.confidence_scores?.[score.vendor_name]?.warranty_months ?? 100;
                      return (
                        <td key={score.vendor_name} className={score.vendor_name === displayAnalysis.recommended_vendor ? 'highlight-col tour-step-confidence' : ''}>
                          {displayAnalysis.warranty_comparison[score.vendor_name]} Months
                          <ConfidenceBar score={warrantyConf} />
                        </td>
                      );
                    })}
                  </tr>
                  <tr>
                    <td><strong>Lead Time</strong></td>
                    {displayAnalysis.vendor_scores.map(score => {
                      const deliveryConf = displayAnalysis.confidence_scores?.[score.vendor_name]?.delivery_days ?? 100;
                      return (
                        <td key={score.vendor_name} className={score.vendor_name === displayAnalysis.recommended_vendor ? 'highlight-col tour-step-confidence' : ''}>
                          {displayAnalysis.delivery_comparison[score.vendor_name]} Days
                          <ConfidenceBar score={deliveryConf} />
                        </td>
                      );
                    })}
                  </tr>
                </tbody>
              </table>
            </div>
          </Card>
        </div>

        <div className="side-panels">
          {/* Risk Flags */}
          <Card className="risk-panel">
            <div className="panel-header">
              <AlertTriangle className="text-warning" size={24} />
              <h3>Identified Risks</h3>
            </div>
            
            {displayAnalysis.risk_flags.length === 0 ? (
              <p className="no-data">No major risks identified.</p>
            ) : (
              <ul className="risk-list">
                {displayAnalysis.risk_flags.map((risk, i) => (
                  <li key={i} className="risk-item">
                    <Badge variant={getBadgeVariant(risk.level)}>{risk.level}</Badge>
                    <div className="risk-details">
                      <strong>Vendor: {risk.vendor_name}</strong>
                      <p>{risk.description}</p>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </Card>

          {/* Savings Opportunities */}
          <Card className="savings-panel">
            <div className="panel-header">
              <TrendingDown className="text-success" size={24} />
              <h3>Savings Opportunities</h3>
            </div>
            
            {displayAnalysis.savings_opportunities.length === 0 ? (
              <p className="no-data">The recommended vendor optimizes for warranty and delivery speed over unit cost.</p>
            ) : (
              <ul className="savings-list">
                {displayAnalysis.savings_opportunities.map((saving, i) => (
                  <li key={i} className="saving-item">
                    <div className="saving-amount">
                      Save ₹{saving.savings_amount.toLocaleString()} 
                      <Badge variant="success" className="ml-2">{saving.savings_percentage}%</Badge>
                    </div>
                    <p>by choosing {saving.cheaper_vendor} over {saving.expensive_vendor}</p>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </div>
      </div>

      {/* Clause Risk Matrix — always shown, graceful fallback when data unavailable */}
      {(() => {
        const vendors = displayAnalysis.vendor_scores.map(s => s.vendor_name);
        const clauses: { key: keyof VendorClauseAnalysis; label: string; description: string }[] = [
          { key: 'payment_terms', label: 'Payment Terms',      description: 'When does the first payment fall due?' },
          { key: 'penalty',       label: 'Penalty / LD Clause', description: 'How much does the vendor pay for late delivery?' },
          { key: 'liability',     label: 'Liability Cap',       description: "Is the vendor's financial exposure capped?" },
          { key: 'force_majeure', label: 'Force Majeure',       description: 'Can the vendor escape penalties by citing external events?' },
        ];
        const riskIcon = (level: RiskLevel) =>
          level === 'HIGH' ? '🔴' : level === 'MEDIUM' ? '🟡' : '🟢';

        const noData = !displayAnalysis.contract_analysis;

        return (
          <div className="clause-matrix-section">
            <h3>
              <FileText size={20} style={{ display: 'inline', marginRight: 8, color: 'var(--accent-primary)' }} />
              Contract Clause Risk Matrix
            </h3>
            <div className="clause-legend">
              <span><span className="legend-dot high"></span> High Risk (buyer exposed)</span>
              <span><span className="legend-dot medium"></span> Medium Risk (some exposure)</span>
              <span><span className="legend-dot low"></span> Low Risk (buyer protected)</span>
              {noData && <span style={{ marginLeft: 'auto', color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.82rem' }}>⚠ Re-upload PDFs to extract clause data</span>}
            </div>
            <Card className="table-card">
              <div className="table-responsive">
                <table className="clause-table">
                  <thead>
                    <tr>
                      <th>Clause</th>
                      {vendors.map(v => (
                        <th key={v} className={v === displayAnalysis.recommended_vendor ? 'highlight-col' : ''}>
                          {v}
                          {v === displayAnalysis.recommended_vendor && (
                            <span style={{ marginLeft: 8, fontSize: '0.75rem', background: '#dcfce7', color: '#15803d', padding: '2px 8px', borderRadius: 12, fontWeight: 700 }}>Winner</span>
                          )}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {clauses.map(({ key, label, description }) => (
                      <tr key={key}>
                        <td className="clause-row-label">
                          {label}
                          <small>{description}</small>
                        </td>
                        {vendors.map(v => {
                          const ca = displayAnalysis.contract_analysis?.[v];
                          const clause: ClauseRisk = ca
                            ? ca[key]
                            : { extracted_value: 'Not extracted yet', risk_level: 'MEDIUM' as RiskLevel };
                          const lvl = clause.risk_level.toLowerCase();
                          return (
                            <td key={v} className={`clause-cell ${v === displayAnalysis.recommended_vendor ? 'clause-col-highlight' : ''}`}>
                              <div className="clause-cell-inner">
                                <span className={`clause-badge ${lvl}`}>
                                  {riskIcon(clause.risk_level)} {clause.risk_level}
                                </span>
                                <span className="clause-value">{clause.extracted_value}</span>
                                {clause.note && <span className="clause-note">{clause.note}</span>}
                              </div>
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>
        );
      })()}
    </div>
  );
}
