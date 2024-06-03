// services/index.ts or services/index.js (depending on your file structure)

export interface NearestPlace {
  name: string;
  elevation: number;
  latitude: number;
  longitude: number;
  continent: string;
  country: string;
  region: string;
  subregion: string;
}

// Adjust the fetchNearestPlace function to properly type the return value
export const fetchNearestPlace = async (latitude: number, longitude: number): Promise<NearestPlace> => {
  try {
    console.log(`Fetching nearest place for coordinates: (${latitude}, ${longitude})`);
    const response = await fetch(`/api/nearest-place/?latitude=${latitude}&longitude=${longitude}`);
    console.log('API response:', response);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error response from server:', errorText);
      throw new Error(`Failed to fetch nearest place: ${response.status} ${response.statusText}`);
    }

    const data = await response.json() as NearestPlace;
    console.log('API response data:', data);
    return data;
  } catch (error) {
    console.error('Error in fetchNearestPlace:', error);
    throw error;
  }
};
