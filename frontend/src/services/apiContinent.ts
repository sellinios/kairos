export interface Country {
  id: number;
  name: string;
  iso_alpha2?: string;
  iso_alpha3?: string;
  iso_numeric?: string;
  capital?: string;
  official_languages?: string;
  currency?: string;
  area?: number;
}

export interface Continent {
  name: string;
  countries: Country[];
}

export const getContinent = async (continentName: string): Promise<Continent> => {
  const response = await fetch(`https://kairos.gr/api/continents/${continentName}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const data: Continent = await response.json();
  return data;
};

export const getCountriesInContinent = async (continentName: string): Promise<Country[]> => {
  const response = await fetch(`https://kairos.gr/api/continents/${continentName}/countries`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const data: Country[] = await response.json();
  return data;
};
