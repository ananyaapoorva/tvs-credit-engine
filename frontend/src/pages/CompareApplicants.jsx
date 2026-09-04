import React, { useState, useEffect } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const CompareApplicants = () => {
  const [customers, setCustomers] = useState([]);
  const [selectedCustomer1, setSelectedCustomer1] = useState('');
  const [selectedCustomer2, setSelectedCustomer2] = useState('');
  const [compareData, setCompareData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [customersLoading, setCustomersLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/credit/customers`);
        const data = await response.json();
        setCustomers(data);
      } catch (err) {
        setError('Failed to fetch customers. Is the backend running?');
      } finally {
        setCustomersLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  const handleCompare = async () => {
    if (!selectedCustomer1 || !selectedCustomer2) return;
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/credit/compare?customer_id_1=${selectedCustomer1}&customer_id_2=${selectedCustomer2}`, {
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
    <div className="container" style={{ paddingBottom: '4rem' }}>
      <div className="page-header reveal-on-scroll">
        <h1 className="page-title">Compare Applicants</h1>
        <p className="page-subtitle">Select two previously scored applicants to view a side-by-side risk profile comparison.</p>
      </div>

      <div className="card reveal-on-scroll">
        {customersLoading ? (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <div className="spinner" style={{ margin: '0 auto' }} />
            <p className="loading-text">Loading applicants...</p>
          </div>
        ) : customers.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem 1.5rem' }}>
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginBottom: '1rem' }}>
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--text-primary)' }}>No Applicants Yet</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', maxWidth: '400px', margin: '0 auto' }}>
              Submit at least two credit applications from the Dashboard to compare their risk profiles here.
            </p>
          </div>
        ) : (
          <>
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
              disabled={!selectedCustomer1 || !selectedCustomer2 || selectedCustomer1 === selectedCustomer2 || loading}
            >
              {loading ? 'Comparing...' : 'Compare Risk Profiles'}
            </button>
            {selectedCustomer1 && selectedCustomer2 && selectedCustomer1 === selectedCustomer2 && (
              <p className="form-error" style={{ marginTop: '0.75rem' }}>Please select two different applicants.</p>
            )}
          </>
        )}
        {error && <p className="form-error" style={{ marginTop: '1rem' }}>{error}</p>}
      </div>

      {compareData && compareData.customer_1 && compareData.customer_2 && (
        <div style={{ marginTop: '2rem' }}>
          <div className="card reveal-on-scroll" style={{ marginBottom: '2rem' }}>
            <h3 className="card-title" style={{ textAlign: 'center', marginBottom: '1rem' }}>Risk Signature Comparison</h3>
            <div style={{ height: '400px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={formatChartData(compareData.customer_1, compareData.customer_2)}>
                  <PolarGrid stroke="var(--border)" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--text-secondary)' }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="none" tick={false} />
                  <Radar name={customers.find(c => c.customer_id === selectedCustomer1)?.name || "Applicant 1"} dataKey="A" stroke="var(--primary)" fill="var(--primary)" fillOpacity={0.3} />
                  <Radar name={customers.find(c => c.customer_id === selectedCustomer2)?.name || "Applicant 2"} dataKey="B" stroke="var(--warning)" fill="var(--warning)" fillOpacity={0.3} />
                  <Tooltip />
                  <Legend />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="results-grid">
            {/* Applicant 1 */}
            <div className="card reveal-on-scroll">
              <h3 className="card-title" style={{ color: 'var(--primary)' }}>{customers.find(c => c.customer_id === selectedCustomer1)?.name || "Applicant 1"}</h3>
              <div className="risk-gauge-container">
                <div className="risk-gauge-score">{Math.round(compareData.customer_1.overall_risk_score)}</div>
                <div className="risk-gauge-label">Score</div>
              </div>
              <p style={{ textAlign: 'center', fontWeight: 500, marginBottom: '1rem', color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.5 }}>{compareData.customer_1.explainability.summary}</p>
            </div>
            
            {/* Applicant 2 */}
            <div className="card reveal-on-scroll">
              <h3 className="card-title" style={{ color: 'var(--warning)' }}>{customers.find(c => c.customer_id === selectedCustomer2)?.name || "Applicant 2"}</h3>
              <div className="risk-gauge-container">
                <div className="risk-gauge-score">{Math.round(compareData.customer_2.overall_risk_score)}</div>
                <div className="risk-gauge-label">Score</div>
              </div>
              <p style={{ textAlign: 'center', fontWeight: 500, marginBottom: '1rem', color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.5 }}>{compareData.customer_2.explainability.summary}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CompareApplicants;
