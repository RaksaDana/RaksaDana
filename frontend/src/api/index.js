import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 30000,
});

// GET /api/v1/tickers
export const getTickers = () => api.get('/api/v1/tickers');

// GET /api/v1/predict/{ticker}?narrate=true
export const getPredict = (ticker) =>
  api.get(`/api/v1/predict/${ticker}`, { params: { narrate: true } });

// GET /api/v1/forecast/{ticker}?days=30
export const getForecast = (ticker, days = 30) =>
  api.get(`/api/v1/forecast/${ticker}`, { params: { days } });

// GET /api/v1/metrics/{ticker}
export const getMetrics = (ticker) => api.get(`/api/v1/metrics/${ticker}`);

// POST /api/v1/profit-loss?narrate=true
export const postProfitLoss = (body) =>
  api.post('/api/v1/profit-loss', body, { params: { narrate: true } });
