import { useState } from 'react';

const RiskGauge = ({ score = 0, riskCategory = 'high', confidence = 0 }) => {
  const radius = 85;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getColor = () => {
    if (score >= 70) return 'var(--success)';
    if (score >= 40) return 'var(--warning)';
    return 'var(--danger)';
  };

  const getCategoryLabel = () => {
    switch (riskCategory) {
      case 'low': return 'Low Risk';
      case 'medium': return 'Medium Risk';
      case 'high': return 'High Risk';
      default: return riskCategory;
    }
  };

  return (
    <div className="risk-gauge-container animate-in">
      <div className="risk-gauge">
        <svg width="200" height="200" viewBox="0 0 200 200">
          <circle className="risk-gauge-bg" cx="100" cy="100" r={radius} />
          <circle
            className="risk-gauge-fill"
            cx="100" cy="100" r={radius}
            stroke={getColor()}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
        </svg>
        <div className="risk-gauge-center">
          <div className="risk-gauge-score" style={{ color: getColor() }}>
            {score.toFixed(1)}
          </div>
          <div className="risk-gauge-label" style={{ color: getColor() }}>
            {getCategoryLabel()}
          </div>
        </div>
      </div>
      <div className="confidence-bar" style={{ width: '100%', marginTop: '1rem' }}>
        <span className="confidence-label">Confidence</span>
        <div className="confidence-track">
          <div className="confidence-fill" style={{ width: `${confidence}%` }} />
        </div>
        <span className="confidence-value">{confidence.toFixed(0)}%</span>
      </div>
    </div>
  );
};

export default RiskGauge;
