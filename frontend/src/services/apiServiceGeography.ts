// src/services/apiServiceGeography.ts
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

interface Place {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

// Fetch the nearest place
export const fetchNearestPlace = async (latitude: number, longitude: number): Promise<Place> => {
  try {
    const response = await axios.get<Place>(`${BASE_URL}/api/places/nearest/`, {
      params: { latitude, longitude }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching nearest place:', error);
    throw error;
  }
};
