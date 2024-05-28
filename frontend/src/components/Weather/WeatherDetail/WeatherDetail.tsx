import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchWeather, fetchPlaceDetails, Weather, WeatherPlace } from '../../../services';

const WeatherDetail: React.FC = () => {
  const { continent, country, region, municipality, placeSlug } = useParams<{
    continent: string;
    country: string;
    region: string;
    municipality: string;
    placeSlug: string;
  }>();

  const [place, setPlace] = useState<WeatherPlace | null>(null);
  const [weather, setWeather] = useState<Weather | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const placeDetails = await fetchPlaceDetails(placeSlug!);
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
      {weather && (
        <>
          {Object.entries(weather).map(([key, value]) => (
            <p key={key}>{key.replace(/_/g, ' ')}: {String(value)}</p>
          ))}
        </>
      )}
    </div>
  );
};

export default WeatherDetail;
