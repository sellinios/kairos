export interface Place {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

export const fetchPlaceList = async (): Promise<Place[]> => {
  const response = await fetch('https://kairos.gr/api/places');
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const data: Place[] = await response.json();
  return data;
};
