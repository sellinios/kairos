import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import DailyPanel from '../DailyPanel';
import { Forecast, DailyForecast } from '../types';
import SunnyIcon from '../Icons/SunnyIcon';
import RainyIcon from '../Icons/RainyIcon';
import CloudyIcon from '../Icons/CloudyIcon';
import './WeatherPage.css';

const countryTimeZones: { [key: string]: string } = {
  'greece': 'Europe/Athens',
  'japan': 'Asia/Tokyo',
  // Add more countries and their time zones here as needed
};

const WeatherPage: React.FC = () => {
  const { continent, country, region, subregion, city } = useParams<{
    continent: string;
    country: string;
    region: string;
    subregion: string;
    city: string;
  }>();

  const [dailyForecasts, setDailyForecasts] = useState<DailyForecast[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const url = `/api/weather/${continent}/${country}/${region}/${subregion}/${city}/`;
        console.log(`Fetching data from ${url}`);
        const response = await fetch(url);
        if (!response.ok) {
          const errorText = await response.text();
          console.error(`Error response from server: ${errorText}`);
          throw new Error(`Failed to fetch weather data: ${response.status} ${response.statusText}`);
        }
        const data: Forecast[] = await response.json();
        const dailyData = processDailyData(data);
        const filteredDailyData = dailyData.filter(daily => new Date(daily.date).getTime() >= new Date().setHours(0, 0, 0, 0));
        setDailyForecasts(filteredDailyData);
      } catch (err) {
        if (err instanceof Error) {
          setError(`Error fetching weather data: ${err.message}`);
          console.error('Error fetching weather data:', err);
        } else {
          setError('An unknown error occurred');
          console.error('An unknown error occurred:', err);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchWeatherData();
  }, [continent, country, region, subregion, city]);

  const processDailyData = (data: Forecast[]): DailyForecast[] => {
    const groupedByDate = data.reduce((acc: { [key: string]: Forecast[] }, curr) => {
      const date = curr.date;
      if (!acc[date]) {
        acc[date] = [];
      }
      acc[date].push(curr);
      return acc;
    }, {});

    return Object.keys(groupedByDate).map(date => {
      const dailyData = groupedByDate[date];
      const minTemp = Math.min(...dailyData.map(f => f.temperature_celsius));
      const maxTemp = Math.max(...dailyData.map(f => f.temperature_celsius));
      const generalIcon = getGeneralIcon(dailyData);
      const generalText = getGeneralText(dailyData);
      return {
        date,
        minTemp,
        maxTemp,
        generalIcon,
        generalText,
        hourlyForecasts: dailyData
      };
    });
  };

  const getGeneralIcon = (dailyData: Forecast[]): JSX.Element => {
    let rain = false;
    let cloudy = false;
    let sunny = false;

    dailyData.forEach(forecast => {
      if (forecast.forecast_data.precipitation_rate_level_0_surface > 0) {
        rain = true;
      } else if (forecast.forecast_data.high_cloud_cover_level_0_highCloudLayer > 50) {
        cloudy = true;
      } else {
        sunny = true;
      }
    });

    if (rain) return <RainyIcon className="icon" />;
    if (cloudy) return <CloudyIcon className="icon" />;
    return <SunnyIcon className="icon" />;
  };

  const getGeneralText = (dailyData: Forecast[]): string => {
    let windy = false;
    dailyData.forEach(forecast => {
      if (forecast.wind_speed > 5) {
        windy = true;
      }
    });
    return windy ? 'Windy' : '';
  };

  return (
    <div className="weather-page">
      <h2>Weather for {city}</h2>
      {dailyForecasts.length > 0 ? (
        <div className="daily-panels">
          {dailyForecasts.map((daily, idx) => (
            <DailyPanel key={idx} forecasts={[daily]} country={country || ''} showHeaders={idx === 0} />
          ))}
        </div>
      ) : (
        <p>No weather data available.</p>
      )}
    </div>
  );
};

export default WeatherPage;
