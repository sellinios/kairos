import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

export interface NearestPlace {
  id: number;
  name: string;
  slug: string;
  longitude: number;
  latitude: number;
  elevation: number;
  confirmed: boolean;
  location: string;
  category: number;
  admin_division: number;
}

export const fetchNearestPlace = async (latitude: number, longitude: number): Promise<NearestPlace> => {
  try {
    const response = await axios.get<NearestPlace>(`${BASE_URL}/api/nearest-place/`, {
      params: { latitude, longitude }
    });
    console.log('API Response:', response.data); // Detailed logging of API response
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Error fetching nearest place:', error.response ? error.response.data : error.message);
    } else {
      console.error('Unknown error:', error);
    }
    throw error;
  }
};
