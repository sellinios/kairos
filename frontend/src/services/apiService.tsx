import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

export const fetchNearestPlace = async (latitude: number, longitude: number): Promise<any> => {
  try {
    const response = await axios.get(`${BASE_URL}/api/places/nearest/`, {
      params: {
        latitude,
        longitude
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
