import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VITE_APP_API_BASE_URL || 'http://localhost:3000/api',
});

export default apiClient;