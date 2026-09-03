import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { submitCreditApplication, fetchMockCustomers } from '../services/api';

const OCCUPATIONS = [
  { value: 'gig_worker', label: 'Gig Worker' },
  { value: 'small_merchant', label: 'Small Merchant' },
  { value: 'informal_sector', label: 'Informal Sector' },
  { value: 'first_time_borrower', label: 'First-time Borrower' },
  { value: 'other', label: 'Other' },
];

const VEHICLE_TYPES = [
  { value: 'none', label: 'No Vehicle' },
  { value: 'two_wheeler', label: 'Two Wheeler' },
  { value: 'three_wheeler', label: 'Three Wheeler' },
  { value: 'car', label: 'Car' },
  { value: 'commercial', label: 'Commercial Vehicle' },
];

const BUSINESS_TYPES = [
  { value: 'retail', label: 'Retail' },
  { value: 'wholesale', label: 'Wholesale' },
  { value: 'service', label: 'Service' },
  { value: 'manufacturing', label: 'Manufacturing' },
  { value: 'other', label: 'Other' },
];

const initialState = {
  name: '', phone_number: '', email: '', date_of_birth: '',
  occupation: 'small_merchant', loan_amount_requested: '',
  gst_data: { annual_turnover: '', filing_consistency: 80, months_filed: '', business_type: 'retail' },
  upi_data: { monthly_transaction_volume: '', transaction_frequency: '', average_transaction_size: '', months_active: '' },
  telecom_data: { monthly_recharge_amount: '', recharge_consistency: 90, months_of_history: '' },
  utility_data: { monthly_bill_amount: '', payment_timeliness: 85, months_of_history: '' },
  ecommerce_data: { purchase_frequency: '', average_order_value: '', return_rate: 5, months_active: '' },
  mobility_data: { vehicle_ownership: false, vehicle_type: 'none', fuel_expense_monthly: '', months_tracked: '' },
};

const ApplicationForm = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialState);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  const handleChange = (section, field, value) => {
    if (section) {
      setForm(prev => ({ ...prev, [section]: { ...prev[section], [field]: value } }));
    } else {
      setForm(prev => ({ ...prev, [field]: value }));
    }
    setErrors(prev => ({ ...prev, [`${section || ''}${field}`]: '' }));
  };

  const validate = () => {
    const errs = {};
    if (!form.name || form.name.length < 2) errs.name = 'Name must be at least 2 characters';
    if (!/^[6-9]\d{9}$/.test(form.phone_number)) errs.phone_number = 'Invalid Indian phone number';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) errs.email = 'Invalid email address';
    if (!form.date_of_birth) errs.date_of_birth = 'Date of birth is required';
    if (!form.loan_amount_requested || Number(form.loan_amount_requested) <= 0) errs.loan_amount_requested = 'Enter a valid loan amount';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const buildPayload = () => {
    const toNum = (v, fallback = 0) => (v === '' || v === undefined || v === null) ? fallback : Number(v);
    return {
      ...form,
      loan_amount_requested: toNum(form.loan_amount_requested),
      gst_data: {
        annual_turnover: toNum(form.gst_data.annual_turnover),
        filing_consistency: form.gst_data.filing_consistency / 100,
        months_filed: toNum(form.gst_data.months_filed),
        business_type: form.gst_data.business_type,
      },
      upi_data: {
        monthly_transaction_volume: toNum(form.upi_data.monthly_transaction_volume),
        transaction_frequency: toNum(form.upi_data.transaction_frequency),
        average_transaction_size: toNum(form.upi_data.average_transaction_size),
        months_active: toNum(form.upi_data.months_active),
      },
      telecom_data: {
        monthly_recharge_amount: toNum(form.telecom_data.monthly_recharge_amount),
        recharge_consistency: form.telecom_data.recharge_consistency / 100,
        months_of_history: toNum(form.telecom_data.months_of_history),
      },
      utility_data: {
        monthly_bill_amount: toNum(form.utility_data.monthly_bill_amount),
        payment_timeliness: form.utility_data.payment_timeliness / 100,
        months_of_history: toNum(form.utility_data.months_of_history),
      },
      ecommerce_data: {
        purchase_frequency: toNum(form.ecommerce_data.purchase_frequency),
        average_order_value: toNum(form.ecommerce_data.average_order_value),
        return_rate: form.ecommerce_data.return_rate / 100,
        months_active: toNum(form.ecommerce_data.months_active),
      },
      mobility_data: {
        vehicle_ownership: form.mobility_data.vehicle_ownership,
        vehicle_type: form.mobility_data.vehicle_type,
        fuel_expense_monthly: toNum(form.mobility_data.fuel_expense_monthly),
        months_tracked: toNum(form.mobility_data.months_tracked),
      },
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');
    if (!validate()) return;
    setLoading(true);
    try {
      const payload = buildPayload();
      const result = await submitCreditApplication(payload);
      navigate(`/results/${result.score_id}`, { state: { scoreData: result } });
    } catch (err) {
      setApiError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const loadMockData = async (index) => {
    try {
      const customers = await fetchMockCustomers();
      const mock = customers[index];
      setForm({
        name: mock.name,
        phone_number: mock.phone_number,
        email: mock.email,
        date_of_birth: mock.date_of_birth,
        occupation: mock.occupation,
        loan_amount_requested: mock.loan_amount_requested,
        gst_data: {
          annual_turnover: mock.gst_data.annual_turnover,
          filing_consistency: Math.round(mock.gst_data.filing_consistency * 100),
          months_filed: mock.gst_data.months_filed,
          business_type: mock.gst_data.business_type,
        },
        upi_data: mock.upi_data,
        telecom_data: {
          monthly_recharge_amount: mock.telecom_data.monthly_recharge_amount,
          recharge_consistency: Math.round(mock.telecom_data.recharge_consistency * 100),
          months_of_history: mock.telecom_data.months_of_history,
        },
        utility_data: {
          monthly_bill_amount: mock.utility_data.monthly_bill_amount,
          payment_timeliness: Math.round(mock.utility_data.payment_timeliness * 100),
          months_of_history: mock.utility_data.months_of_history,
        },
        ecommerce_data: {
          purchase_frequency: mock.ecommerce_data.purchase_frequency,
          average_order_value: mock.ecommerce_data.average_order_value,
          return_rate: Math.round(mock.ecommerce_data.return_rate * 100),
          months_active: mock.ecommerce_data.months_active,
        },
        mobility_data: mock.mobility_data,
      });
      setErrors({});
      setApiError('');
    } catch {
      setApiError('Failed to load mock data. Is the backend running?');
    }
  };

  const renderInput = (label, section, field, type = 'text', placeholder = '', sublabel = '') => (
    <div className="form-group">
      <label className="form-label">
        {label}
        {sublabel && <span className="form-sublabel"> — {sublabel}</span>}
      </label>
      <input
        type={type}
        className={`form-input ${errors[`${section || ''}${field}`] ? 'error' : ''}`}
        value={section ? form[section][field] : form[field]}
        onChange={(e) => handleChange(section, field, type === 'number' ? e.target.value : e.target.value)}
        placeholder={placeholder}
      />
      {errors[`${section || ''}${field}`] && (
        <div className="form-error">{errors[`${section || ''}${field}`]}</div>
      )}
    </div>
  );

  const renderSlider = (label, section, field, min = 0, max = 100, sublabel = '') => (
    <div className="form-group">
      <label className="form-label">
        {label}
        {sublabel && <span className="form-sublabel"> — {sublabel}</span>}
      </label>
      <div className="slider-group">
        <input
          type="range"
          min={min}
          max={max}
          value={form[section][field]}
          onChange={(e) => handleChange(section, field, Number(e.target.value))}
        />
        <span className="slider-value">{form[section][field]}%</span>
      </div>
    </div>
  );

  return (
    <form onSubmit={handleSubmit} id="credit-application-form">
      {loading && (
        <div className="loading-overlay">
          <div className="spinner" />
          <div className="loading-text">Calculating your credit score...</div>
        </div>
      )}

      {/* Mock Data Quick Fill */}
      <div className="card" style={{ marginBottom: '1.5rem', background: 'var(--primary-50)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          <span style={{ fontWeight: 600, fontSize: '0.85rem' }}>⚡ Quick Fill:</span>
          {['Rajesh (Merchant)', 'Priya (Gig)', 'Mohammed (Wholesale)', 'Lakshmi (Informal)', 'Arjun (New)'].map((label, i) => (
            <button key={i} type="button" className="btn btn-sm btn-secondary"
              onClick={() => loadMockData(i)}>
              {label}
            </button>
          ))}
        </div>
      </div>

      {apiError && (
        <div style={{ background: 'var(--danger-bg)', color: 'var(--danger)', padding: '1rem', borderRadius: 'var(--radius-md)', marginBottom: '1rem', fontWeight: 500 }}>
          {apiError}
        </div>
      )}

      {/* Personal Information */}
      <div className="form-section">
        <h3 className="form-section-title">👤 Personal Information</h3>
        <div className="form-row">
          {renderInput('Full Name', null, 'name', 'text', 'Enter full name')}
          {renderInput('Phone Number', null, 'phone_number', 'tel', '9876543210')}
        </div>
        <div className="form-row">
          {renderInput('Email Address', null, 'email', 'email', 'you@example.com')}
          {renderInput('Date of Birth', null, 'date_of_birth', 'date')}
        </div>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Occupation</label>
            <select className="form-select" value={form.occupation}
              onChange={(e) => handleChange(null, 'occupation', e.target.value)}>
              {OCCUPATIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>
          {renderInput('Loan Amount (₹)', null, 'loan_amount_requested', 'number', '50000')}
        </div>
      </div>

      {/* GST Data */}
      <div className="form-section">
        <h3 className="form-section-title">📊 GST Data</h3>
        <div className="form-row">
          {renderInput('Annual Turnover', 'gst_data', 'annual_turnover', 'number', '₹ Amount', 'in INR')}
          {renderInput('Months Filed (Last 12)', 'gst_data', 'months_filed', 'number', '0-12')}
        </div>
        <div className="form-row">
          {renderSlider('Filing Consistency', 'gst_data', 'filing_consistency', 0, 100, '% of filings on time')}
          <div className="form-group">
            <label className="form-label">Business Type</label>
            <select className="form-select" value={form.gst_data.business_type}
              onChange={(e) => handleChange('gst_data', 'business_type', e.target.value)}>
              {BUSINESS_TYPES.map(b => <option key={b.value} value={b.value}>{b.label}</option>)}
            </select>
          </div>
        </div>
      </div>

      {/* UPI Data */}
      <div className="form-section">
        <h3 className="form-section-title">💳 UPI Transaction Trends</h3>
        <div className="form-row">
          {renderInput('Monthly Transaction Volume', 'upi_data', 'monthly_transaction_volume', 'number', '₹ Amount', 'in INR')}
          {renderInput('Transaction Frequency', 'upi_data', 'transaction_frequency', 'number', 'per month')}
        </div>
        <div className="form-row">
          {renderInput('Average Transaction Size', 'upi_data', 'average_transaction_size', 'number', '₹ Amount')}
          {renderInput('Months Active', 'upi_data', 'months_active', 'number', 'months')}
        </div>
      </div>

      {/* Telecom Data */}
      <div className="form-section">
        <h3 className="form-section-title">📱 Telecom Data</h3>
        <div className="form-row">
          {renderInput('Monthly Recharge (₹)', 'telecom_data', 'monthly_recharge_amount', 'number', '₹ Amount')}
          {renderInput('Months of History', 'telecom_data', 'months_of_history', 'number', 'months')}
        </div>
        {renderSlider('Recharge Consistency', 'telecom_data', 'recharge_consistency', 0, 100, '% on-time recharges')}
      </div>

      {/* Utility Data */}
      <div className="form-section">
        <h3 className="form-section-title">💡 Utility Payments</h3>
        <div className="form-row">
          {renderInput('Monthly Bill Amount (₹)', 'utility_data', 'monthly_bill_amount', 'number', '₹ Amount')}
          {renderInput('Months of History', 'utility_data', 'months_of_history', 'number', 'months')}
        </div>
        {renderSlider('Payment Timeliness', 'utility_data', 'payment_timeliness', 0, 100, '% paid on time')}
      </div>

      {/* E-commerce Data */}
      <div className="form-section">
        <h3 className="form-section-title">🛒 E-commerce Activity</h3>
        <div className="form-row">
          {renderInput('Purchase Frequency', 'ecommerce_data', 'purchase_frequency', 'number', 'purchases/month')}
          {renderInput('Average Order Value (₹)', 'ecommerce_data', 'average_order_value', 'number', '₹ Amount')}
        </div>
        <div className="form-row">
          {renderSlider('Return Rate', 'ecommerce_data', 'return_rate', 0, 100, '% of orders returned')}
          {renderInput('Months Active', 'ecommerce_data', 'months_active', 'number', 'months')}
        </div>
      </div>

      {/* Mobility Data */}
      <div className="form-section">
        <h3 className="form-section-title">🚗 Mobility & Vehicle Usage</h3>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Vehicle Ownership</label>
            <div className="toggle-wrapper">
              <button type="button"
                className={`toggle ${form.mobility_data.vehicle_ownership ? 'active' : ''}`}
                onClick={() => handleChange('mobility_data', 'vehicle_ownership', !form.mobility_data.vehicle_ownership)}
              />
              <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                {form.mobility_data.vehicle_ownership ? 'Yes' : 'No'}
              </span>
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Vehicle Type</label>
            <select className="form-select" value={form.mobility_data.vehicle_type}
              onChange={(e) => handleChange('mobility_data', 'vehicle_type', e.target.value)}
              disabled={!form.mobility_data.vehicle_ownership}>
              {VEHICLE_TYPES.map(v => <option key={v.value} value={v.value}>{v.label}</option>)}
            </select>
          </div>
        </div>
        <div className="form-row">
          {renderInput('Monthly Fuel Expense (₹)', 'mobility_data', 'fuel_expense_monthly', 'number', '₹ Amount')}
          {renderInput('Months Tracked', 'mobility_data', 'months_tracked', 'number', 'months')}
        </div>
      </div>

      {/* Submit */}
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '1rem' }}>
        <button type="button" className="btn btn-secondary" onClick={() => setForm(initialState)}>
          Reset Form
        </button>
        <button type="submit" className="btn btn-primary btn-lg" disabled={loading} id="submit-application">
          {loading ? 'Calculating...' : '🚀 Calculate Credit Score'}
        </button>
      </div>
    </form>
  );
};

export default ApplicationForm;
