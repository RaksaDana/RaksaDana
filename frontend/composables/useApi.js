import axios from 'axios';
import { ref } from 'vue';
import { useRuntimeConfig } from '#app';

export const useApi = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;
  
  const apiClient = axios.create({
    baseURL: apiBase,
    headers: {
      'Content-Type': 'application/json'
    }
  });

  const withRetry = async (requestFn, retries = 1) => {
    let attempt = 0;
    while(attempt <= retries) {
      try {
        return await requestFn();
      } catch (err) {
        if (attempt < retries && !err.response) {
          attempt++;
        } else {
          throw err;
        }
      }
    }
  };
  
  const createEndpoint = (requestFnBuilder) => {
    return (...args) => {
      const data = ref(null);
      const loading = ref(false);
      const error = ref(null);

      const fetch = async () => {
        loading.value = true;
        error.value = null;
        try {
          const response = await withRetry(() => requestFnBuilder(...args)());
          data.value = response.data;
        } catch (err) {
          error.value = err.response?.data?.message || err.message || 'Terjadi kesalahan pada server.';
          console.error('API Error:', err);
        } finally {
          loading.value = false;
        }
        return data.value;
      };

      return { data, loading, error, fetch };
    };
  };

  const getTickers = createEndpoint(() => () => apiClient.get('/api/v1/tickers'));
  const getPrediction = createEndpoint((ticker) => () => apiClient.get(`/api/v1/predict/${ticker}`));
  const getPredictionWithNarration = createEndpoint((ticker) => () => apiClient.get(`/api/v1/predict/${ticker}?narrate=true`));
  const getForecast = createEndpoint((ticker, days = 30) => () => apiClient.get(`/api/v1/forecast/${ticker}?days=${days}`));
  const getMetrics = createEndpoint((ticker) => () => apiClient.get(`/api/v1/metrics/${ticker}`));
  const calculateProfitLoss = createEndpoint((payload) => () => apiClient.post('/api/v1/profit-loss', payload));
  const calculateProfitLossWithNarration = createEndpoint((payload) => () => apiClient.post('/api/v1/profit-loss?narrate=true', payload));

  return {
    getTickers,
    getPrediction,
    getPredictionWithNarration,
    getForecast,
    getMetrics,
    calculateProfitLoss,
    calculateProfitLossWithNarration
  };
};
