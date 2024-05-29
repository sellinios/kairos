import React, { useState, useEffect } from 'react';
import { fetchPlaceList, Place } from '../../services';

const PlaceList: React.FC = () => {
  const [places, setPlaces] = useState<Place[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const placesData = await fetchPlaceList();
        setPlaces(placesData);
      } catch (err) {
        setError('Failed to fetch places');
      } finally {
        setLoading(false);
      }
    };

    fetchPlaces();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Places</h1>
      <ul>
        {places.map((place) => (
          <li key={place.id}>
            <h2>{place.admin_division.name}</h2>
            <p>Latitude: {place.latitude}</p>
            <p>Longitude: {place.longitude}</p>
            <p>Elevation: {place.elevation}</p>
            <a href={place.url}>More Info</a>
            <a href={place.weather_url}>Weather Info</a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PlaceList;
