import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import WeatherBlock from '../Weather/WeatherBlock/WeatherBlock';
import MetarBlock from '../Weather/MetarBlock/MetarBlock';
import './Home.css';

interface Forecast {
  id: number;
  temperature: number;
  precipitation: number | null;
  wind_speed: number | null;
  timestamp: string;
  place: number;
  weatherCondition?: 'Clear Day' | 'Partly Cloudy' | 'Rain';
}

interface MetarData {
  station: string;
  metar_text: string;
  metar_timestamp: string;
}

interface HomeProps {
  latitude: number;
  longitude: number;
  location: string;
}

const Home: React.FC<HomeProps> = ({ latitude, longitude, location }) => {
  const { t } = useTranslation('Home'); // Specify the namespace
  const [locationData, setLocationData] = useState<{
    current: { temperature: number; condition: 'Clear Day' | 'Partly Cloudy' | 'Rain'; windSpeed: number };
    forecast: Forecast[];
  } | null>(null);
  const [metarData, setMetarData] = useState<MetarData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [weatherError, setWeatherError] = useState<string>('');
  const [metarError, setMetarError] = useState<string>('');

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const currentResponse = await axios.get('https://kairos.gr/api/weather/current/');
        const forecastResponse = await axios.get('https://kairos.gr/api/weather/forecast/');

        console.log('Current weather response:', currentResponse.data);
        console.log('Forecast weather response:', forecastResponse.data);

        const currentWeather = currentResponse.data;
        const forecastWeather = forecastResponse.data.map((item: Forecast) => ({
          id: item.id,
          temperature: item.temperature,
          precipitation: item.precipitation,
          wind_speed: item.wind_speed,
          timestamp: item.timestamp,
          place: item.place,
          weatherCondition: 'Clear Day' as 'Clear Day' // Default value, replace with actual logic
        }));

        // Sort the forecastWeather by timestamp
        forecastWeather.sort((a: Forecast, b: Forecast) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

        const formattedData = {
          current: {
            temperature: currentWeather.temperature,
            condition: 'Clear Day' as 'Clear Day', // Default value, replace with actual logic
            windSpeed: currentWeather.wind_speed ?? 0, // Default to 0 if null
          },
          forecast: forecastWeather
        };

        setLocationData(formattedData);
      } catch (error) {
        console.error('Error fetching weather data:', error);
        setWeatherError(t('weatherFetchError'));
      } finally {
        setIsLoading(false);
      }
    };

    const fetchMetarData = async () => {
      try {
        const metarResponse = await axios.get('https://kairos.gr/api/weather/metar/', {
          params: { latitude, longitude }
        });
        console.log('METAR response:', metarResponse.data);
        setMetarData(metarResponse.data);
      } catch (error) {
        console.error('Error fetching METAR data:', error);
        setMetarError(t('metarFetchError'));
      }
    };

    fetchWeatherData();
    fetchMetarData();
  }, [latitude, longitude, t]);

  if (isLoading) {
    return <div>{t('loading')}</div>;
  }

  return (
    <div className="container home-container">
      <Helmet>
        <title>{t('homeTitle')} - Kairos Weather</title>
        <meta name="description" content={`${t('weatherDescription')} ${location}. ${t('stayUpdated')}`} />
        <meta name="keywords" content={`weather, forecast, ${location} weather, Kairos Weather`} />
        <meta property="og:title" content={`${t('weatherIn')} ${location} - Kairos Weather`} />
        <meta property="og:description" content={`${t('currentWeather')} ${location} ${t('kairosWeather')}`} />
        <meta property="og:url" content="https://kairos.gr" />
        <link rel="canonical" href="https://kairos.gr" />
      </Helmet>
      {weatherError ? <div>{t('error')}: {weatherError}</div> : locationData && <WeatherBlock location={location} locationData={locationData} />}
      {metarError ? <div>{t('error')}: {metarError}</div> : metarData.length > 0 && <MetarBlock metarData={metarData} />}
    </div>
  );
}

export default Home;
