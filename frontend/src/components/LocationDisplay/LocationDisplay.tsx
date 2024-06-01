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
  const [continent, setContinent] = useState<string>('unknown');
  const [country, setCountry] = useState<string>('unknown');
  const [region, setRegion] = useState<string>('unknown');
  const [subregion, setSubregion] = useState<string>('unknown');
  const [city, setCity] = useState<string>('unknown');

  useEffect(() => {
    const fetchLocation = async () => {
      try {
        console.log(`Fetching nearest place for coordinates: (${latitude}, ${longitude})`);
        const place: NearestPlace = await fetchNearestPlace(latitude, longitude);
        console.log('Fetched place:', place); // Log the place object

        if (place && typeof place.name === 'string' && typeof place.elevation === 'number' && typeof place.latitude === 'number' && typeof place.longitude === 'number') {
          setEntityName(place.name);
          setElevation(place.elevation);
          setCity(place.name);
          setContinent(place.continent || 'unknown');
          setCountry(place.country || 'unknown');
          setRegion(place.region || 'unknown');
          setSubregion(place.subregion || 'unknown');
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

  const formatUrl = (continent: string, country: string, region: string, subregion: string, city: string) => {
    const urlName = city.toLowerCase().replace(/ /g, '-');
    return `https://kairos.gr/weather/${continent}/${country}/${region}/${subregion}/${urlName}/`;
  };

  return (
    <div className="location-display">
      <h1 className="h4">{entityName || 'Loading...'}</h1>
      <p>Elevation: {elevation !== null ? `${elevation} meters` : 'Loading...'}</p>
      {entityName && (
        <a href={formatUrl(continent, country, region, subregion, city)} target="_blank" rel="noopener noreferrer">
          View weather for {entityName}
        </a>
      )}
    </div>
  );
};

export default LocationDisplay;
