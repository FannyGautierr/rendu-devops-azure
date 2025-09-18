import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:3000/api',
});

export default apiClient;