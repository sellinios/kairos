import React, { useEffect, useState } from 'react';
import LocationDisplay from '../LocationDisplay/LocationDisplay';
import './UpperHeader.css'; // Import the CSS file

interface UpperHeaderProps {
  onLocationUpdate?: (location: string, latitude: number, longitude: number) => void;
}

const UpperHeader: React.FC<UpperHeaderProps> = ({ onLocationUpdate = () => {} }) => {
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCoordinates = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
          setLatitude(position.coords.latitude);
          setLongitude(position.coords.longitude);
          setLoading(false);
        }, (err) => {
          console.error('Error getting geolocation:', err);
          setError('Error getting geolocation');
          setLoading(false);
        });
      } else {
        console.error('Geolocation is not supported by this browser.');
        setError('Geolocation is not supported by this browser.');
        setLoading(false);
      }
    };

    fetchCoordinates();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <header className="upper-header d-flex align-items-center p-3 bg-light">
      <LocationDisplay
        latitude={latitude!}
        longitude={longitude!}
        onLocationUpdate={onLocationUpdate}
      />
    </header>
  );
};

export default UpperHeader;