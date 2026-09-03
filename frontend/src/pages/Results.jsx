import { useState, useEffect } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import { fetchCreditScore } from '../services/api';
import RiskGauge from '../components/RiskGauge';
import ResultsDashboard from '../components/ResultsDashboard';
import ExplainabilityCard from '../components/ExplainabilityCard';
import TransactionHistory from '../components/TransactionHistory';

const Results = () => {
  const { scoreId } = useParams();
  const location = useLocation();
  const [scoreData, setScoreData] = useState(location.state?.scoreData || null);
  const [loading, setLoading] = useState(!scoreData);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!scoreData && scoreId) {
      loadScore();
    }
  }, [scoreId]);

  const loadScore = async () => {
    setLoading(true);
    try {
      const data = await fetchCreditScore(scoreId);
      setScoreData(data);
    } catch (err) {
      setError(err.message || 'Failed to load score data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container" style={{ padding: '4rem 0', textAlign: 'center' }}>
        <div className="spinner" style={{ margin: '0 auto' }} />
        <p className="loading-text">Loading results...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container" style={{ padding: '4rem 0', textAlign: 'center' }}>
        <div className="card">
          <h2 style={{ color: 'var(--danger)' }}>Error</h2>
          <p>{error}</p>
          <Link to="/" className="btn btn-primary" style={{ marginTop: '1rem' }}>Return Home</Link>
        </div>
      </div>
    );
  }

  if (!scoreData) return null;

  return (
    <div className="container" style={{ paddingBottom: '4rem' }}>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 className="page-title">Credit Assessment Results</h1>
          <p className="page-subtitle">ID: {scoreData.score_id}</p>
        </div>
        <Link to="/" className="btn btn-outline btn-sm">← Back to New Application</Link>
      </div>

      <div className="results-grid">
        <div className="results-sidebar">
          <div className="card animate-in">
            <div className="card-header">
              <h3 className="card-title">Overall Risk Score</h3>
            </div>
            <RiskGauge 
              score={scoreData.overall_risk_score} 
              riskCategory={scoreData.risk_category} 
              confidence={scoreData.confidence_score * 100}
            />
          </div>
          
          <ResultsDashboard scoreData={scoreData} />
        </div>

        <div className="results-main">
          <ExplainabilityCard explainability={scoreData.explainability} />
          <TransactionHistory />
        </div>
      </div>
    </div>
  );
};

export default Results;
