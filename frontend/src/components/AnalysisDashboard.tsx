"use client";

import React from 'react';
import { Trophy, AlertTriangle, TrendingDown, DollarSign, Clock, ShieldCheck } from 'lucide-react';
import { ProcurementAnalysis, RiskFlag } from '../services/types';
import { Card } from './ui/Card';
import { Badge } from './ui/Badge';
import './AnalysisDashboard.css';

interface Props {
  analysis: ProcurementAnalysis;
}

export function AnalysisDashboard({ analysis }: Props) {
  const getBadgeVariant = (level: string) => {
    switch (level) {
      case 'RiskLevel.HIGH': return 'error';
      case 'RiskLevel.MEDIUM': return 'warning';
      default: return 'info';
    }
  };

  return (
    <div className="dashboard-container animate-fade-in">
      
      {/* Recommended Vendor Hero */}
      <Card className="hero-card">
        <div className="hero-content">
          <div className="hero-icon">
            <Trophy size={48} />
          </div>
          <div className="hero-text">
            <h2>Recommended: {analysis.recommended_vendor}</h2>
            <p>{analysis.recommendation_reason}</p>
          </div>
        </div>
      </Card>

      <div className="dashboard-grid">
        {/* Vendor Rankings */}
        <div className="rankings-section">
          <h3>Vendor Rankings & Scores</h3>
          <div className="rankings-list">
            {analysis.vendor_scores.map((score) => {
              const totalCost = analysis.cost_comparison[score.vendor_name];
              const warranty = analysis.warranty_comparison[score.vendor_name];
              const delivery = analysis.delivery_comparison[score.vendor_name];
              const isWinner = score.vendor_name === analysis.recommended_vendor;

              return (
                <Card key={score.vendor_name} className={`ranking-card ${isWinner ? 'winner' : ''}`}>
                  <div className="ranking-header">
                    <div className="rank-badge">#{score.rank}</div>
                    <h4>{score.vendor_name}</h4>
                    <div className="overall-score">
                      {score.overall_score.toFixed(1)} / 100
                    </div>
                  </div>
                  
                  <div className="metrics-grid">
                    <div className="metric">
                      <DollarSign size={16} />
                      <span>₹{totalCost.toLocaleString()}</span>
                      <small>Score: {score.cost_score}</small>
                    </div>
                    <div className="metric">
                      <ShieldCheck size={16} />
                      <span>{warranty} Months</span>
                      <small>Score: {score.warranty_score}</small>
                    </div>
                    <div className="metric">
                      <Clock size={16} />
                      <span>{delivery} Days</span>
                      <small>Score: {score.delivery_score}</small>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>

        <div className="side-panels">
          {/* Risk Flags */}
          <Card className="risk-panel">
            <div className="panel-header">
              <AlertTriangle className="text-warning" size={24} />
              <h3>Identified Risks</h3>
            </div>
            
            {analysis.risk_flags.length === 0 ? (
              <p className="no-data">No major risks identified.</p>
            ) : (
              <ul className="risk-list">
                {analysis.risk_flags.map((risk, i) => (
                  <li key={i} className="risk-item">
                    <Badge variant={getBadgeVariant(risk.level)}>{risk.level.split('.')[1]}</Badge>
                    <div className="risk-details">
                      <strong>{risk.vendor_name}</strong>
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
            
            {analysis.savings_opportunities.length === 0 ? (
              <p className="no-data">No cost savings available (recommended vendor is most expensive).</p>
            ) : (
              <ul className="savings-list">
                {analysis.savings_opportunities.map((saving, i) => (
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
    </div>
  );
}
