import axios from 'axios';

const API_URL = 'http://localhost:5000/api/incidents';

export const fetchRecentIncidents = async (limit = 5) => {
  try {
    const response = await axios.get(`${API_URL}?limit=${limit}&page=1`);
    return response.data.incidents;
  } catch (error) {
    console.error('Error fetching recent incidents:', error);
    return [];
  }
};

export const fetchIncidentDetails = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching incident details:', error);
    return null;
  }
};

export const fetchIncidentStats = async () => {
  try {
    const response = await axios.get(`${API_URL}/stats/overview`);
    return response.data;
  } catch (error) {
    console.error('Error fetching incident stats:', error);
    return {};
  }
};

export const searchIncidents = async (filters) => {
  // Convert filters to query parameters
  const queryString = Object.keys(filters)
    .filter(key => filters[key] !== '')
    .map(key => `${key}=${encodeURIComponent(filters[key])}`)
    .join('&'); 

  try {
    const response = await axios.get(`${API_URL}?${queryString}`);
    return response.data;
  } catch (error) {
    console.error('Error searching incidents:', error);
    return { incidents: [], totalPages: 0 };
  }
};

export default {
  fetchRecentIncidents,
  fetchIncidentDetails,
  fetchIncidentStats,
  searchIncidents
};