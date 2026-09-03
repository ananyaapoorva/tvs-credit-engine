const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Submit a credit application and receive a risk score.
 */
export const submitCreditApplication = async (formData) => {
  const response = await fetch(`${API_BASE_URL}/credit/score`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to calculate credit score' }));
    throw new Error(error.detail || 'Failed to calculate credit score');
  }

  return response.json();
};

/**
 * Retrieve a previously calculated credit score by ID.
 */
export const fetchCreditScore = async (scoreId) => {
  const response = await fetch(`${API_BASE_URL}/credit/score/${scoreId}`);
  if (!response.ok) throw new Error('Score not found');
  return response.json();
};

/**
 * Get all scores for a specific customer.
 */
export const fetchCustomerScores = async (customerId) => {
  const response = await fetch(`${API_BASE_URL}/credit/customer/${customerId}/scores`);
  if (!response.ok) throw new Error('Customer not found');
  return response.json();
};

/**
 * Get all mock customer profiles.
 */
export const fetchMockCustomers = async () => {
  const response = await fetch(`${API_BASE_URL}/credit/mock-customers`);
  if (!response.ok) throw new Error('Failed to fetch mock customers');
  return response.json();
};

/**
 * Health check.
 */
export const healthCheck = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
};
