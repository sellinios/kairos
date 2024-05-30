import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

export interface Place {
  id: number;
  name: string;
  longitude: number;
  latitude: number;
  elevation: number;
  category: {
    id: number;
    name: string;
  };
  admin_division: {
    id: number;
    name: string;
    slug: string;
    parent: number | null;
  };
  url: string;
  weather_url: string;
}

export const fetchNearestPlace = async (latitude: number, longitude: number): Promise<Place> => {
  try {
    const response = await axios.get<Place>(`${BASE_URL}/places/nearest/`, {
      params: { latitude, longitude }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching nearest place:', error);
    throw error;
  }
};
