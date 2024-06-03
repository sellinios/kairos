export interface Region {
  id: number;
  name: string;
  continent: string;
  description?: string; // Assuming description is a possible field
}

export const getRegion = async (continent: string, region: string): Promise<Region> => {
  const response = await fetch(`https://kairos.gr/api/regions/${continent}/${region}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const data: Region = await response.json();
  return data;
};
