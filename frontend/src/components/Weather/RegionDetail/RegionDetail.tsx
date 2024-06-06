import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getRegion, Region } from '../../../services';

const RegionDetail: React.FC = () => {
  const { continent, region } = useParams<{ continent: string; region: string }>();
  const [regionData, setRegionData] = useState<Region | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (continent && region) {
      getRegion(continent, region)
        .then(response => {
          setRegionData(response);
          setLoading(false);
        })
        .catch((error: any) => {
          console.error("There was an error fetching the region data!", error);
          setError('There was an error fetching the region data!');
          setLoading(false);
        });
    }
  }, [continent, region]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>{regionData?.name}</h1>
      <p>{regionData?.description}</p>
    </div>
  );
};

export default RegionDetail;
