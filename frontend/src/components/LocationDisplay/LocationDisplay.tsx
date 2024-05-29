import React, { useState, useEffect } from 'react';
import { fetchNearestPlace, Place } from '../../services/';

interface LocationDisplayProps {
  latitude: number;
  longitude: number;
  onLocationUpdate: (name: string, latitude: number, longitude: number) => void;
}

const LocationDisplay: React.FC<LocationDisplayProps> = ({ latitude, longitude, onLocationUpdate }) => {
  const [entityName, setEntityName] = useState<string | null>(null);
  const [elevation, setElevation] = useState<number | null>(null);
  const [fetchError, setFetchError] = useState<boolean>(false);

  useEffect(() => {
    const fetchLocation = async () => {
      try {
        const place: Place = await fetchNearestPlace(latitude, longitude);
        console.log(place); // Verify the place object structure
        setEntityName(place.name);
        setElevation(place.elevation);
        setFetchError(false);
        onLocationUpdate(place.name, latitude, longitude);
        localStorage.setItem('entityName', place.name);
      } catch (error) {
        setFetchError(true);
      }
    };

    fetchLocation();
  }, [latitude, longitude, onLocationUpdate]);

  if (fetchError) {
    return <div>Error fetching location.</div>;
  }

  return (
    <div>
      <h1>{entityName}</h1>
      <p>Elevation: {elevation} meters</p>
    </div>
  );
};

export default LocationDisplay;
