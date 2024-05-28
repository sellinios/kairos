import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

export interface Weather {
  timestamp: string;
  forecast_data: Record<string, any>;
}

export interface WeatherPlace {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
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
}

export const fetchWeather = async (latitude: number, longitude: number): Promise<Weather[]> => {
  try {
    const response = await axios.get<Weather[]>(`${BASE_URL}/api/weather/nearest/`, {
      params: { latitude, longitude }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching weather data:', error);
    throw error;
  }
};

export const fetchNearestPlaceDetails = async (latitude: number, longitude: number): Promise<WeatherPlace> => {
  try {
    const response = await axios.get<WeatherPlace>(`${BASE_URL}/api/places/nearest/`, {
      params: { latitude, longitude }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching nearest place details:', error);
    throw error;
  }
};
