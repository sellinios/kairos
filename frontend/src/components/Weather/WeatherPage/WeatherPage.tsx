import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchWeather, fetchNearestPlaceDetails, Weather, WeatherPlace } from '../../../services';

const WeatherPage: React.FC = () => {
  const { latitude, longitude } = useParams<{ latitude: string; longitude: string }>();

  const [place, setPlace] = useState<WeatherPlace | null>(null);
  const [weather, setWeather] = useState<Weather[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWeatherData = async () => {
      if (!latitude || !longitude) {
        setError('Latitude or longitude is undefined');
        setLoading(false);
        return;
      }

      try {
        const lat = parseFloat(latitude);
        const lon = parseFloat(longitude);

        console.log('Fetching nearest place details for coordinates:', { latitude, longitude });
        const placeDetails = await fetchNearestPlaceDetails(lat, lon);
        setPlace(placeDetails);

        console.log('Fetching weather data for place:', placeDetails);
        const weatherData = await fetchWeather(lat, lon);
        setWeather(weatherData);

        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch weather data:', err);
        setError('Failed to fetch weather data');
        setLoading(false);
      }
    };

    fetchWeatherData();
  }, [latitude, longitude]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Weather for {place?.name}</h1>
      {weather && weather.map((forecast, index) => (
        <div key={index}>
          <h2>{forecast.timestamp}</h2>
          {Object.entries(forecast.forecast_data).map(([key, value]) => (
            <p key={key}>{key.replace(/_/g, ' ')}: {String(value)}</p>
          ))}
        </div>
      ))}
    </div>
  );
};

export default WeatherPage;
