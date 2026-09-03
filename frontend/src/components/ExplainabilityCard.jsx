const ExplainabilityCard = ({ explainability }) => {
  if (!explainability) return null;

  const { factors = [], summary = '', recommendation = '' } = explainability;

  const getIcon = (impact) => {
    switch (impact) {
      case 'positive': return '✓';
      case 'negative': return '✗';
      default: return '●';
    }
  };

  return (
    <div className="card animate-in animate-delay-3">
      <div className="card-header">
        <h3 className="card-title"> Risk Factor Analysis</h3>
      </div>

      <div className="factor-list">
        {factors.map((factor, index) => (
          <div key={index} className={`factor-item ${factor.impact}`}>
            <div className={`factor-icon ${factor.impact}`}>
              {getIcon(factor.impact)}
            </div>
            <div className="factor-content">
              <div className="factor-category">{factor.category}</div>
              <div className="factor-signal">{factor.signal}</div>
              <div className="factor-explanation">{factor.explanation}</div>
              <div className={`factor-contribution`} style={{
                color: factor.impact === 'positive' ? 'var(--success)' :
                       factor.impact === 'negative' ? 'var(--danger)' : 'var(--warning)'
              }}>
                {factor.contribution}
              </div>
            </div>
          </div>
        ))}
      </div>

      {(summary || recommendation) && (
        <div className="summary-panel" style={{ marginTop: '1.5rem' }}>
          {summary && <p className="summary-text">{summary}</p>}
          {recommendation && (
            <div className="recommendation-panel">
              <h4> Recommendation</h4>
              <p>{recommendation}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ExplainabilityCard;
