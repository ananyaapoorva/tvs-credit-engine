import { useState } from 'react';
import ApplicationForm from '../components/ApplicationForm';

const Dashboard = () => {
  return (
    <>
      <div className="hero">
        <div className="hero-content">
          <h1>Alternative Data Credit Scoring Engine</h1>
          <p>
            AI-powered explainable risk scores for first-time borrowers, gig workers, small merchants, and the informal sector using alternative data sources.
          </p>
          <div className="hero-cta">
            <a href="#application-form" className="btn btn-primary btn-lg">
              Start Application
            </a>
          </div>
        </div>
      </div>

      <div className="features-section">
        <div className="container">
          <h2>Why Alternative Data?</h2>
          <p className="subtitle">Moving beyond traditional credit bureaus to score the unbanked and underbanked.</p>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon"></div>
              <h3>GST & Digital Trails</h3>
              <p>Analyze business health and compliance through GST filing consistency and turnover.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon"></div>
              <h3>UPI & Cashflow</h3>
              <p>Understand real-time income and expense patterns through UPI transaction volumes and velocity.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon"></div>
              <h3>Utility & Telecom</h3>
              <p>Evaluate financial discipline via bill payment timeliness and telecom recharge consistency.</p>
            </div>
          </div>
        </div>
      </div>

      <div className="container page-header" id="application-form">
        <h2 className="page-title">New Credit Application</h2>
        <p className="page-subtitle">Fill in the details or use quick-fill mock profiles below.</p>
      </div>

      <div className="container" style={{ paddingBottom: '4rem' }}>
        <ApplicationForm />
      </div>
    </>
  );
};

export default Dashboard;
