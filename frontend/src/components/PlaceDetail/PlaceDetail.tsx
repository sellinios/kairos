import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

interface Place {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

const PlaceDetail: React.FC = () => {
  const { placeName } = useParams<{ placeName: string }>();
  const [place, setPlace] = useState<Place | null>(null);
  const [forecast, setForecast] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlaceData = async () => {
      try {
        const placeResponse = await axios.get(`/api/geography/places/?name=${placeName}`);
        if (placeResponse.data.length > 0) {
          setPlace(placeResponse.data[0]);
          const forecastResponse = await axios.get(`/api/geography/places/${placeResponse.data[0].id}/forecast/`);
          setForecast(forecastResponse.data);
        } else {
          setError('Place not found');
        }
      } catch (error) {
        console.error('Error fetching place data:', error);
        setError('Place not found');
      }
    };

    fetchPlaceData();
  }, [placeName]);

  if (error) {
    return <div>{error}</div>;
  }

  if (!place) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{place.name}</h1>
      <p>Latitude: {place.latitude}</p>
      <p>Longitude: {place.longitude}</p>
      <Link to={`/weather/${placeName}`}>Check Weather</Link>
      {forecast && (
        <div>
          <h2>Weather Forecast</h2>
          <pre>{JSON.stringify(forecast, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default PlaceDetail;
