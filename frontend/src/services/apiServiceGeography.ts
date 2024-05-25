// src/services/apiServiceGeography.ts
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

export interface Place {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

export interface Country {
  id: number;
  name: string;
  iso_alpha2?: string;
  iso_alpha3?: string;
  iso_numeric?: number;
  capital?: string;
  official_languages?: string;
  currency?: string;
  area?: number;
}

export interface Continent {
  id: number;
  name: string;
  countries: Country[]; // Add the countries property
}

export interface Region {
  id: number;
  name: string;
  description?: string;
  // Add other fields as necessary
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

// Fetch all continents
export const getContinents = async (): Promise<Continent[]> => {
  try {
    const response = await axios.get<Continent[]>(`${BASE_URL}/api/continents/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching continents:', error);
    throw error;
  }
};

// Fetch a specific continent by name
export const getContinent = async (name: string): Promise<Continent> => {
  try {
    const response = await axios.get<Continent>(`${BASE_URL}/api/continents/${name}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching continent ${name}:`, error);
    throw error;
  }
};

// Fetch a specific region within a continent
export const getRegion = async (continent: string, region: string): Promise<Region> => {
  try {
    const response = await axios.get<Region>(`${BASE_URL}/api/continents/${continent}/greece/${region}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching region ${region} in continent ${continent}:`, error);
    throw error;
  }
};
