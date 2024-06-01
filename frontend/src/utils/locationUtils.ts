export const formatPlaceNameForURL = (placeName: string): string => {
  return placeName.toLowerCase().replace(/\s+/g, '-');
};

export const generateWeatherURL = (continent: string, country: string, region: string, subregion: string, city: string): string => {
  return `/weather/${continent}/${country}/${region}/${subregion}/${city}`;
};

export const generateWeatherAPIURL = (continent: string, country: string, region: string, subregion: string, city: string): string => {
  return `/api/weather/${continent}/${country}/${region}/${subregion}/${city}/`;
};
