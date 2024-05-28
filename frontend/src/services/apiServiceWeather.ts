import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

export interface Weather {
  temperature: number;
  description: string;
  // Add other weather-related fields as needed
}

export interface WeatherPlace { // Use alias here
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  elevation: number; // Ensure this matches your model
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

export const fetchWeather = async (latitude: number, longitude: number): Promise<Weather> => {
  try {
    const response = await axios.get<Weather>(`${BASE_URL}/api/weather/`, {
      params: { latitude, longitude }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching weather data:', error);
    throw error;
  }
};

export const fetchPlaceDetails = async (slug: string): Promise<WeatherPlace> => { // Use alias here
  try {
    const response = await axios.get<WeatherPlace>(`${BASE_URL}/api/places/${slug}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching place details:', error);
    throw error;
  }
};
