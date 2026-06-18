import React from 'react';
import './ui.css';

interface ConfidenceBarProps {
  score: number;
}

export function ConfidenceBar({ score }: ConfidenceBarProps) {
  const getColor = (s: number) => {
    if (s >= 80) return 'var(--success)';
    if (s >= 50) return 'var(--warning)';
    return 'var(--error)';
  };

  const getLabel = (s: number) => {
    if (s >= 80) return 'High Confidence';
    if (s >= 50) return 'Medium Confidence';
    return 'Low Confidence / Missing';
  };

  const color = getColor(score);
  const label = getLabel(score);

  return (
    <div className="confidence-container" title={label}>
      <div className="confidence-track">
        <div 
          className="confidence-fill" 
          style={{ 
            width: `${Math.max(0, Math.min(100, score))}%`, 
            backgroundColor: color 
          }} 
        />
      </div>
      <span className="confidence-text" style={{ color }}>{score}%</span>
    </div>
  );
}
