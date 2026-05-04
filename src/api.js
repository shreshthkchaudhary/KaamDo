import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('kaamdo_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── Auth ──
export const registerUser = (data) => api.post('/auth/register', data);
export const loginUser = (data) => api.post('/auth/login', data);
export const getMe = () => api.get('/auth/me');

// ── Tasks ──
export const createTask = (data) => {
  if (data instanceof FormData) {
    return api.post('/tasks', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  }
  return api.post('/tasks', data);
};
export const getTasks = (params) => api.get('/tasks', { params });
export const getTask = (id) => api.get(`/tasks/${id}`);
export const updateTaskStatus = (id, status) =>
  api.patch(`/tasks/${id}/status`, { status });

// ── Bids ──
export const placeBid = (data) => api.post('/bids', data);
export const getTaskBids = (taskId) => api.get(`/tasks/${taskId}/bids`);
export const acceptBid = (bidId) => api.patch(`/bids/${bidId}/accept`);
export const getMyBids = () => api.get('/bids/my');

// ── AI ──
export const classifyTask = (description) =>
  api.post('/ai/classify', { description });
export const estimatePrice = (category, radius_km) =>
  api.post('/ai/estimate-price', { category, radius_km });
export const matchWorkers = (task_id) =>
  api.post('/ai/match-workers', { task_id });

// ── Ratings ──
export const submitRating = (data) => api.post('/ratings', data);
export const getUserRatings = (userId) => api.get(`/users/${userId}/ratings`);

export default api;
