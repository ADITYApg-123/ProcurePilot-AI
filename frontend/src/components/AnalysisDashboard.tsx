"use client";

import React from 'react';
import { Trophy, AlertTriangle, TrendingDown, DollarSign, Clock, ShieldCheck, Download } from 'lucide-react';
import { ProcurementAnalysis, RiskFlag } from '../services/types';
import { Card } from './ui/Card';
import { Badge } from './ui/Badge';
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

  return (
    <div className="dashboard-container animate-fade-in">
      
      {/* Recommended Vendor Hero */}
      <Card className="hero-card">
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
      <Card className="scenario-engine-card">
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

      <div className="dashboard-grid">
        {/* Vendor Rankings */}
        <div className="rankings-section">
          <h3>Vendor Rankings & Scores</h3>
          <div className="rankings-list">
            {displayAnalysis.vendor_scores.map((score) => {
              const totalCost = displayAnalysis.cost_comparison[score.vendor_name];
              const warranty = displayAnalysis.warranty_comparison[score.vendor_name];
              const delivery = displayAnalysis.delivery_comparison[score.vendor_name];
              const isWinner = score.vendor_name === displayAnalysis.recommended_vendor;

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
                      <small>Cost Score: {score.cost_score}</small>
                    </div>
                    <div className="metric">
                      <ShieldCheck size={16} />
                      <span>{warranty} Months</span>
                      <small>Warranty Score: {score.warranty_score}</small>
                    </div>
                    <div className="metric">
                      <Clock size={16} />
                      <span>{delivery} Days</span>
                      <small>Delivery Score: {score.delivery_score}</small>
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
    </div>
  );
}
