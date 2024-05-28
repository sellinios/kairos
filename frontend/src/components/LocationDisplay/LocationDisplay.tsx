import React, { useState, useEffect } from 'react';
import { fetchNearestPlace, Place } from '../../services/';

interface LocationDisplayProps {
  onLocationUpdate: (name: string, latitude: number, longitude: number) => void;
}

const LocationDisplay: React.FC<LocationDisplayProps> = ({ onLocationUpdate }) => {
  const [entityName, setEntityName] = useState<string | null>(null);
  const [elevation, setElevation] = useState<number | null>(null);
  const [fetchError, setFetchError] = useState<boolean>(false);

  useEffect(() => {
    const fetchLocation = async () => {
      try {
        const latitude = 37.7749;  // Example latitude, replace with actual value
        const longitude = -122.4194;  // Example longitude, replace with actual value

        const place: Place = await fetchNearestPlace(latitude, longitude);
        setEntityName(place.name);
        setElevation(place.elevation);  // Using the elevation property
        setFetchError(false);
        onLocationUpdate(place.name, latitude, longitude);
        localStorage.setItem('entityName', place.name);
      } catch (error) {
        setFetchError(true);
      }
    };

    fetchLocation();
  }, [onLocationUpdate]);

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
