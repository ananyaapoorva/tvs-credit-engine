import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

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

  const radarData = Object.entries(COMPONENT_LABELS).map(([key, label]) => ({
    subject: label.name,
    A: component_scores[key] ?? 0,
    fullMark: 100,
  }));

  return (
    <div className="card animate-in animate-delay-2">
      <div className="card-header">
        <h3 className="card-title"> Component Score Breakdown</h3>
        <span className={`badge badge-${scoreData.risk_category}`}>
          {scoreData.risk_category?.toUpperCase()} RISK
        </span>
      </div>

      <div style={{ height: '250px', width: '100%', marginBottom: '1.5rem' }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
            <PolarGrid stroke="var(--border)" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--text-secondary)', fontSize: 10 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} stroke="none" />
            <Radar name="Score" dataKey="A" stroke="var(--primary)" fill="var(--primary)" fillOpacity={0.4} />
            <Tooltip />
          </RadarChart>
        </ResponsiveContainer>
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
