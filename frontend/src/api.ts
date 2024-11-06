import axios from 'axios';

// Create an Axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Base URL for your API
  timeout: 10000, // Optional: set a timeout for requests
  // headers: { 'Authorization': 'Bearer YOUR_TOKEN' } // Optional: set default headers
});

// Function to fetch total trials
export const fetchTotalTrials = async () => {
  try {
    const response = await api.get('/trials/total');
    return response.data;
  } catch (error) {
    console.error('Error fetching total trials:', error);
    throw error;
  }
};

// Function to fetch conditions data
export const fetchConditionsData = async () => {
  try {
    const response = await api.get('/trials/conditions');
    return response.data.conditions;
  } catch (error) {
    console.error('Error fetching conditions:', error);
    throw error;
  }
};

// Function to fetch sponsors data
export const fetchSponsorsData = async () => {
  try {
    const response = await api.get('/trials/sponsors');
    return response.data.sponsors;
  } catch (error) {
    console.error('Error fetching sponsors:', error);
    throw error;
  }
};