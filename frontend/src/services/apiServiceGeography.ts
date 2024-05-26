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
  slug: string;
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
  countries: Country[];
}

export interface Region {
  id: number;
  name: string;
  description?: string;
}

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

export const getContinents = async (): Promise<Continent[]> => {
  try {
    const response = await axios.get<Continent[]>(`${BASE_URL}/api/continents/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching continents:', error);
    throw error;
  }
};

export const getContinent = async (name: string): Promise<Continent> => {
  try {
    const response = await axios.get<Continent>(`${BASE_URL}/api/continents/${name}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching continent ${name}:`, error);
    throw error;
  }
};

export const getRegion = async (continent: string, region: string): Promise<Region> => {
  try {
    const response = await axios.get<Region>(`${BASE_URL}/api/continents/${continent}/regions/${region}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching region ${region} in continent ${continent}:`, error);
    throw error;
  }
};

// New function to fetch countries within a continent
export const getCountriesInContinent = async (continent: string): Promise<Country[]> => {
  try {
    const response = await axios.get<Country[]>(`${BASE_URL}/api/continents/${continent}/countries/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching countries in continent ${continent}:`, error);
    throw error;
  }
};
