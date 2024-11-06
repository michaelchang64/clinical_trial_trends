import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

export const fetchTotalTrials = async () => {
  try {
    const response = await api.get('/trials/total');
    return response.data;
  } catch (error) {
    console.error('Error fetching total trials:', error);
    throw error;
  }
};

export const fetchConditionsData = async () => {
  try {
    const response = await api.get('/trials/conditions');
    return response.data.conditions;
  } catch (error) {
    console.error('Error fetching conditions:', error);
    throw error;
  }
};

export const fetchSponsorsData = async () => {
  try {
    const response = await api.get('/trials/sponsors');
    return response.data.sponsors;
  } catch (error) {
    console.error('Error fetching sponsors:', error);
    throw error;
  }
};