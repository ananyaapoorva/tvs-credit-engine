import React, { useState, useEffect } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const CompareApplicants = () => {
  const [customers, setCustomers] = useState([]);
  const [selectedCustomer1, setSelectedCustomer1] = useState('');
  const [selectedCustomer2, setSelectedCustomer2] = useState('');
  const [compareData, setCompareData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch recent customers
    const fetchCustomers = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/credit/customers');
        const data = await response.json();
        setCustomers(data);
      } catch (err) {
        setError('Failed to fetch customers');
      }
    };
    fetchCustomers();
  }, []);

  const handleCompare = async () => {
    if (!selectedCustomer1 || !selectedCustomer2) return;
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/credit/compare?customer_id_1=${selectedCustomer1}&customer_id_2=${selectedCustomer2}`, {
        method: 'POST'
      });
      const data = await response.json();
      setCompareData(data);
    } catch (err) {
      setError('Failed to compare applicants');
    } finally {
      setLoading(false);
    }
  };

  const formatChartData = (c1, c2) => {
    if (!c1 || !c2) return [];
    return [
      { subject: 'GST', A: c1.component_scores.gst_score, B: c2.component_scores.gst_score, fullMark: 100 },
      { subject: 'UPI', A: c1.component_scores.upi_score, B: c2.component_scores.upi_score, fullMark: 100 },
      { subject: 'Telecom', A: c1.component_scores.telecom_score, B: c2.component_scores.telecom_score, fullMark: 100 },
      { subject: 'Utility', A: c1.component_scores.utility_score, B: c2.component_scores.utility_score, fullMark: 100 },
      { subject: 'E-commerce', A: c1.component_scores.ecommerce_score, B: c2.component_scores.ecommerce_score, fullMark: 100 },
      { subject: 'Mobility', A: c1.component_scores.mobility_score, B: c2.component_scores.mobility_score, fullMark: 100 },
    ];
  };

  return (
    <div className="container" style={{ padding: '2rem 1.5rem' }}>
      <div className="card">
        <h2 className="card-title" style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Compare Applicants</h2>
        <div className="form-row" style={{ marginBottom: '1.5rem' }}>
          <div className="form-group">
            <label className="form-label">Applicant 1</label>
            <select className="form-select" value={selectedCustomer1} onChange={(e) => setSelectedCustomer1(e.target.value)}>
              <option value="">Select Applicant</option>
              {customers.map(c => (
                <option key={c.customer_id} value={c.customer_id}>{c.name} ({c.phone_number})</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Applicant 2</label>
            <select className="form-select" value={selectedCustomer2} onChange={(e) => setSelectedCustomer2(e.target.value)}>
              <option value="">Select Applicant</option>
              {customers.map(c => (
                <option key={c.customer_id} value={c.customer_id}>{c.name} ({c.phone_number})</option>
              ))}
            </select>
          </div>
        </div>
        <button 
          className="btn btn-primary" 
          onClick={handleCompare}
          disabled={!selectedCustomer1 || !selectedCustomer2 || loading}
        >
          {loading ? 'Comparing...' : 'Compare Risk Profiles'}
        </button>
        {error && <p className="form-error" style={{ marginTop: '1rem' }}>{error}</p>}
      </div>

      {compareData && compareData.customer_1 && compareData.customer_2 && (
        <div style={{ marginTop: '2rem' }}>
          <div className="card" style={{ marginBottom: '2rem' }}>
            <h3 className="card-title" style={{ textAlign: 'center', marginBottom: '1rem' }}>Risk Signature Comparison</h3>
            <div style={{ height: '400px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={formatChartData(compareData.customer_1, compareData.customer_2)}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="subject" />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} />
                  <Radar name={customers.find(c => c.customer_id === selectedCustomer1)?.name || "Applicant 1"} dataKey="A" stroke="#003C9B" fill="#003C9B" fillOpacity={0.3} />
                  <Radar name={customers.find(c => c.customer_id === selectedCustomer2)?.name || "Applicant 2"} dataKey="B" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.3} />
                  <Tooltip />
                  <Legend />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="results-grid">
            {/* Applicant 1 */}
            <div className="card">
              <h3 className="card-title" style={{ color: '#003C9B' }}>{customers.find(c => c.customer_id === selectedCustomer1)?.name || "Applicant 1"}</h3>
              <div className="risk-gauge-container">
                <div className="risk-gauge-score">{Math.round(compareData.customer_1.overall_risk_score)}</div>
                <div className="risk-gauge-label">Score</div>
              </div>
              <p style={{ textAlign: 'center', fontWeight: 'bold', marginBottom: '1rem' }}>{compareData.customer_1.explainability.summary}</p>
            </div>
            
            {/* Applicant 2 */}
            <div className="card">
              <h3 className="card-title" style={{ color: '#F59E0B' }}>{customers.find(c => c.customer_id === selectedCustomer2)?.name || "Applicant 2"}</h3>
              <div className="risk-gauge-container">
                <div className="risk-gauge-score">{Math.round(compareData.customer_2.overall_risk_score)}</div>
                <div className="risk-gauge-label">Score</div>
              </div>
              <p style={{ textAlign: 'center', fontWeight: 'bold', marginBottom: '1rem' }}>{compareData.customer_2.explainability.summary}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CompareApplicants;
