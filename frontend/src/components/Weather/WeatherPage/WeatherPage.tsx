import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchWeather, fetchPlaceDetails } from '../../../services';

interface Place {
  id: number;
  name: string;
  slug: string;
  longitude: number;
  latitude: number;
  elevation: number;
  category: { id: number; name: string };
  admin_division: { id: number; name: string; slug: string; parent: number | null };
}

interface Weather {
  temperature: number;
  description: string;
  // Add other weather-related fields as needed
}

const WeatherPage: React.FC = () => {
  const { continent, country, region, municipality, placeSlug } = useParams<{
    continent: string;
    country: string;
    region: string;
    municipality: string;
    placeSlug: string;
  }>();

  const [place, setPlace] = useState<Place | null>(null);
  const [weather, setWeather] = useState<Weather[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWeatherData = async () => {
      if (!placeSlug) {
        setError('Place slug is undefined');
        setLoading(false);
        return;
      }

      try {
        const placeDetails = await fetchPlaceDetails(placeSlug);
        setPlace(placeDetails);

        const weatherData = await fetchWeather(placeDetails.latitude, placeDetails.longitude);
        setWeather(weatherData);

        setLoading(false);
      } catch (err) {
        setError('Failed to fetch weather data');
        setLoading(false);
      }
    };

    fetchWeatherData();
  }, [continent, country, region, municipality, placeSlug]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Weather for {place?.name}</h1>
      {weather.length > 0 && weather.map((data, index) => (
        <div key={index}>
          <p>Temperature: {data.temperature}°C</p>
          <p>Description: {data.description}</p>
          {/* Render other weather details here */}
        </div>
      ))}
    </div>
  );
};

export default WeatherPage;
