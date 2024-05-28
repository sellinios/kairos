import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchWeatherData, Weather } from '../../../services';

const WeatherPage: React.FC = () => {
  const { continent, country, region, subregion, city } = useParams<{
    continent: string;
    country: string;
    region: string;
    subregion: string;
    city: string;
  }>();

  const [weather, setWeather] = useState<Weather[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('Received parameters:', { continent, country, region, subregion, city });

    const fetchWeatherDataAsync = async () => {
      if (!continent || !country || !region || !subregion || !city) {
        setError('Some required parameters are missing');
        setLoading(false);
        return;
      }

      try {
        const weatherData = await fetchWeatherData(continent, country, region, subregion, city);
        setWeather(weatherData);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch weather data:', err);
        setError('Failed to fetch weather data');
        setLoading(false);
      }
    };

    fetchWeatherDataAsync();
  }, [continent, country, region, subregion, city]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Weather Data for {city}</h1>
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
