// src/services/locationService.js
import axios from 'axios';

export interface Place {
  name: string;
  elevation: number;
}

export const fetchNearestPlace = async (latitude: number, longitude: number): Promise<Place> => {
  const response = await axios.get(`http://localhost:8000/nearest-place/`, {
    params: { lat: latitude, lon: longitude },
  });
  return response.data;
};
