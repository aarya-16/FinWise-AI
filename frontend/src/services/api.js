import axios from 'axios';

// When serving frontend from backend, use relative /api path
// In dev mode (Vite), use VITE_API_BASE_URL or localhost backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || 
                     (import.meta.env.DEV ? 'http://localhost:8000/api' : '/api');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Transaction APIs
export const createTransaction = async (transactionData) => {
  const response = await api.post('/transactions/', transactionData);
  return response.data;
};

export const getTransactions = async (limit = 100) => {
  const response = await api.get(`/transactions/?limit=${limit}`);
  return response.data;
};

export const uploadTransactionsCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/transactions/bulk', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const deleteTransaction = async (transactionId) => {
  const response = await api.delete(`/transactions/${transactionId}`);
  return response.data;
};

// Insights APIs
export const getInsights = async () => {
  const response = await api.get('/insights/');
  return response.data;
};

// Goals APIs
export const createGoal = async (goalData) => {
  const response = await api.post('/goals/', goalData);
  return response.data;
};

export const getGoals = async () => {
  const response = await api.get('/goals/');
  return response.data;
};

export const updateGoal = async (goalId, updateData) => {
  const response = await api.patch(`/goals/${goalId}`, null, {
    params: updateData,
  });
  return response.data;
};

export const deleteGoal = async (goalId) => {
  const response = await api.delete(`/goals/${goalId}`);
  return response.data;
};

export default api;
