import React, { useEffect, useState } from 'react';
import LocationDisplay from '../LocationDisplay/LocationDisplay';

interface UpperHeaderProps {
  onLocationUpdate?: (location: string, latitude: number, longitude: number) => void;
}

const UpperHeader: React.FC<UpperHeaderProps> = ({ onLocationUpdate = () => {} }) => {
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);

  useEffect(() => {
    const fetchCoordinates = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
          setLatitude(position.coords.latitude);
          setLongitude(position.coords.longitude);
        });
      } else {
        console.error('Geolocation is not supported by this browser.');
      }
    };

    fetchCoordinates();
  }, []);

  if (latitude === null || longitude === null) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <LocationDisplay
        latitude={latitude}
        longitude={longitude}
        onLocationUpdate={onLocationUpdate}
      />
    </div>
  );
};

export default UpperHeader;
