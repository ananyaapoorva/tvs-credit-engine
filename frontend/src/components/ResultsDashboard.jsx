const COMPONENT_LABELS = {
  gst_score: { name: 'GST Filing', emoji: '' },
  upi_score: { name: 'UPI Transactions', emoji: '' },
  telecom_score: { name: 'Telecom Recharge', emoji: '' },
  utility_score: { name: 'Utility Payments', emoji: '' },
  ecommerce_score: { name: 'E-commerce Activity', emoji: '' },
  mobility_score: { name: 'Mobility & Vehicle', emoji: '' },
};

const getBarColor = (score) => {
  if (score >= 70) return 'var(--success)';
  if (score >= 40) return 'var(--warning)';
  return 'var(--danger)';
};

const ResultsDashboard = ({ scoreData }) => {
  if (!scoreData) return null;

  const { component_scores = {} } = scoreData;

  return (
    <div className="card animate-in animate-delay-2">
      <div className="card-header">
        <h3 className="card-title"> Component Score Breakdown</h3>
        <span className={`badge badge-${scoreData.risk_category}`}>
          {scoreData.risk_category?.toUpperCase()} RISK
        </span>
      </div>

      <div>
        {Object.entries(COMPONENT_LABELS).map(([key, label]) => {
          const score = component_scores[key] ?? 0;
          return (
            <div key={key} className="component-bar-wrapper">
              <div className="component-bar-header">
                <span className="component-bar-name">
                  {label.emoji} {label.name}
                </span>
                <span className="component-bar-score" style={{ color: getBarColor(score) }}>
                  {score.toFixed(1)}
                </span>
              </div>
              <div className="component-bar-track">
                <div
                  className="component-bar-fill"
                  style={{
                    width: `${score}%`,
                    background: `linear-gradient(90deg, ${getBarColor(score)}, ${getBarColor(score)}dd)`,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ResultsDashboard;
