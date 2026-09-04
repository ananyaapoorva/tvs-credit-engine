import { useState } from 'react';
import ApplicationForm from '../components/ApplicationForm';

const Dashboard = () => {
  return (
    <>
      <div className="hero liquid-bg">
        <div className="hero-content reveal-on-scroll">
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

      <div className="features-section liquid-bg">
        <div className="container">
          <h2 className="reveal-on-scroll">Why Alternative Data?</h2>
          <p className="subtitle reveal-on-scroll">Moving beyond traditional credit bureaus to score the unbanked and underbanked.</p>
          
          <div className="features-grid">
            <div className="feature-card reveal-on-scroll card" style={{ animationDelay: '0.1s' }}>
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
              </div>
              <h3>GST & Digital Trails</h3>
              <p>Analyze business health and compliance through GST filing consistency and turnover.</p>
            </div>
            <div className="feature-card reveal-on-scroll card" style={{ animationDelay: '0.2s' }}>
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"></path><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"></path><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"></path></svg>
              </div>
              <h3>UPI & Cashflow</h3>
              <p>Understand real-time income and expense patterns through UPI transaction volumes and velocity.</p>
            </div>
            <div className="feature-card reveal-on-scroll card" style={{ animationDelay: '0.3s' }}>
              <div className="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
              </div>
              <h3>Utility & Telecom</h3>
              <p>Evaluate financial discipline via bill payment timeliness and telecom recharge consistency.</p>
            </div>
          </div>
        </div>
      </div>

      <div className="container page-header reveal-on-scroll" id="application-form">
        <h2 className="page-title">New Credit Application</h2>
        <p className="page-subtitle">Fill in the details or use quick-fill mock profiles below.</p>
      </div>

      <div className="container reveal-on-scroll" style={{ paddingBottom: '4rem', animationDelay: '0.1s' }}>
        <ApplicationForm />
      </div>
    </>
  );
};

export default Dashboard;
