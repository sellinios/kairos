import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchWeather, fetchPlaceDetails } from '../../../services/';
import { Place } from '../../../services/';

interface Weather {
  temperature: number;
  description: string;
  details: string;
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
  const [weather, setWeather] = useState<Weather | null>(null); // Ensure this is a single Weather object
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
  }, [placeSlug]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  const weatherDetails = weather ? JSON.parse(weather.details) : {};

  return (
    <div>
      <h1>Weather for {place?.name}</h1>
      {Object.entries(weatherDetails).map(([key, value]) => (
        <div key={key}>
          <p>
            <>
              {key.replace(/_/g, ' ')}: {value}
            </>
          </p>
        </div>
      ))}
    </div>
  );
};

export default WeatherPage;
