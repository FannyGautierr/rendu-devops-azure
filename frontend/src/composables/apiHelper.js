import axios from 'axios';

console.log('🔍 VITE_APP_API_BASE_URL:', import.meta.env.VITE_APP_API_BASE_URL);
console.log('🔍 All env vars:', import.meta.env);

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_APP_API_BASE_URL || 'http://localhost:3000',
});

export default apiClient;