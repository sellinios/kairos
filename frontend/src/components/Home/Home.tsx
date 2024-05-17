import React, { useState, useEffect } from 'react';
import axios from 'axios';
import WeatherBlock from '../WeatherBlock/WeatherBlock';
import './Home.css';

interface Forecast {
  day: string;
  temperature: number;
  weatherCondition: 'Clear Day' | 'Partly Cloudy' | 'Rain';
}

const Home: React.FC = () => {
  const [location, setLocation] = useState<string>('Locating...');
  const [locationData, setLocationData] = useState<{
    current: { temperature: number; condition: 'Clear Day' | 'Partly Cloudy' | 'Rain'; windSpeed: number };
    forecast: Forecast[];
  } | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchLocationData = async (latitude: number, longitude: number) => {
      try {
        setIsLoading(true);

        // Fetch location data
        const locationResponse = await axios.get('/api/geography/places/nearest/', {
          params: { latitude, longitude }
        });
        console.log('Location response:', locationResponse.data);
        setLocation(locationResponse.data.name || 'Unknown Location');

        // Fetch weather data
        const weatherResponse = await axios.get('/api/weather/', {
          params: { latitude, longitude }
        });
        console.log('Weather response:', weatherResponse.data);

        // Process the weather data to get the current and forecast data
        const weatherData = weatherResponse.data;
        const currentWeather = weatherData[weatherData.length - 1];
        const forecastWeather = weatherData.slice(0, -1).map((item: any) => ({
          day: new Date(item.timestamp).toLocaleDateString('en-US', { weekday: 'long' }),
          temperature: item.temperature,
          weatherCondition: 'Clear Day' as 'Clear Day' // Default value, replace with actual logic
        }));

        const formattedData = {
          current: {
            temperature: currentWeather.temperature,
            condition: 'Clear Day' as 'Clear Day', // Default value, replace with actual logic
            windSpeed: currentWeather.wind_speed ?? 0, // Default to 0 if null
          },
          forecast: forecastWeather
        };

        setLocationData(formattedData);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching location or weather data:', error);
        setError('Failed to fetch data');
        setIsLoading(false);
      }
    };

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          fetchLocationData(latitude, longitude);
        },
        (error) => {
          console.error('Geolocation error:', error);
          setLocation('Geolocation not supported');
          setError('Geolocation not supported');
          setIsLoading(false);
        }
      );
    } else {
      setLocation('Geolocation not supported');
      setError('Geolocation not supported');
      setIsLoading(false);
    }
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="container home-container">
      <WeatherBlock location={location} locationData={locationData} />
      <div className="home-content text-center">
        <h1 className="home-title">Welcome to the Home page!</h1>
        <p className="home-text">This is a simple homepage for our React application.</p>
        <button className="btn btn-primary home-button">Learn More</button>
      </div>
    </div>
  );
}

export default Home;
