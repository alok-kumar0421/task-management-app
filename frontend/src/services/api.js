import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
});

export const loginWithGoogle = async (token) => {
  const response = await api.post('/auth/google', { token });
  return response.data;
};

export const fetchTasks = async (userId) => {
  const response = await api.get(`/tasks/?user_id=${userId}`);
  return response.data.tasks;
};

export const createTask = async (taskData) => {
  const response = await api.post('/tasks/', taskData);
  return response.data.task;
};

export const completeTask = async (taskId, userId) => {
  const response = await api.patch(`/tasks/${taskId}/complete`, { user_id: userId });
  return response.data.task;
};

export const fetchUsers = async () => {
  const response = await api.get('/users/');
  return response.data.users;
};
