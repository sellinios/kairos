import React, { useState, useEffect } from 'react';
import { fetchNearestPlace, NearestPlace } from '../../services/';
import './LocationDisplay.css'; // Import the CSS file

interface LocationDisplayProps {
  latitude: number;
  longitude: number;
  onLocationUpdate: (name: string, latitude: number, longitude: number) => void;
}

const LocationDisplay: React.FC<LocationDisplayProps> = ({ latitude, longitude, onLocationUpdate }) => {
  const [entityName, setEntityName] = useState<string | null>(null);
  const [elevation, setElevation] = useState<number | null>(null);
  const [fetchError, setFetchError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLocation = async () => {
      try {
        const place: NearestPlace = await fetchNearestPlace(latitude, longitude);
        console.log('Fetched place:', place); // Log the place object

        if (
          place &&
          typeof place.name === 'string' &&
          typeof place.elevation === 'number' &&
          typeof place.latitude === 'number' &&
          typeof place.longitude === 'number'
        ) {
          setEntityName(place.name);
          setElevation(place.elevation);
          setFetchError(null);
          onLocationUpdate(place.name, latitude, longitude);
          localStorage.setItem('entityName', place.name);
        } else {
          console.error('Invalid place data structure:', place);
          setFetchError('Invalid place data');
        }
      } catch (error) {
        console.error('Error fetching location:', error);
        setFetchError('Error fetching location');
      }
    };

    fetchLocation();
  }, [latitude, longitude, onLocationUpdate]);

  if (fetchError) {
    return <div className="location-display error">{fetchError}</div>;
  }

  return (
    <div className="location-display">
      <h1 className="h4">{entityName || 'Loading...'}</h1>
      <p>Elevation: {elevation !== null ? `${elevation} meters` : 'Loading...'}</p>
    </div>
  );
};

export default LocationDisplay;
