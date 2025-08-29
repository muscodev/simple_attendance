import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // dynamic from .env
  withCredentials: true, // if using cookies for auth
});

api.interceptors.response.use(
  response => response,
  error => {
    // global error handling (e.g., auth)
    if (error.response?.status === 401) {
      // Redirect or notify
    }
    return Promise.reject(error);
  }
);

export default api;
