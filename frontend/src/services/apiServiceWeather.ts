// src/services/apiServiceWeather.ts
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

interface Weather {
  temperature: number;
  description: string;
  // Add other weather-related fields as needed
}

// Fetch weather data
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
