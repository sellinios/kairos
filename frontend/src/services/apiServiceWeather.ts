import axios from 'axios';
import { Place } from './apiServiceGeography'; // Import the Place interface

const BASE_URL = process.env.REACT_APP_API_URL;

interface Weather {
  temperature: number;
  description: string;
  details: string; // Assume details are stored as JSON string
  // Add other weather-related fields as needed
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

export const fetchPlaceDetails = async (slug: string): Promise<Place> => {
  try {
    const response = await axios.get<Place>(`${BASE_URL}/api/places/${slug}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching place details:', error);
    throw error;
  }
};
