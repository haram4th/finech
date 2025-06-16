import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchStocks = async (query: string) => {
  const response = await api.get(`/stocks/search?query=${query}`);
  return response.data;
};

export const getStockInfo = async (symbol: string) => {
  const response = await api.get(`/stocks/${symbol}`);
  return response.data;
};

export const getStockPrice = async (symbol: string) => {
  const response = await api.get(`/stocks/${symbol}/price`);
  return response.data;
};

export const getStockNews = async (symbol: string) => {
  const response = await api.get(`/news/${symbol}`);
  return response.data;
};

export const getPricePrediction = async (symbol: string) => {
  const response = await api.get(`/predictions/${symbol}`);
  return response.data;
}; 