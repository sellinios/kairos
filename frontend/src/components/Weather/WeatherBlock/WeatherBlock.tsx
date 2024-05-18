// frontend/src/components/Weather/WeatherBlock/WeatherBlock.tsx

import React from 'react';
import './WeatherBlock.css';

interface Forecast {
  id: number;
  temperature: number;
  precipitation: number | null;
  wind_speed: number | null;
  timestamp: string;
  place: number;
  weatherCondition?: 'Clear Day' | 'Partly Cloudy' | 'Rain';
}

interface WeatherData {
  current: {
    temperature: number;
    condition: 'Clear Day' | 'Partly Cloudy' | 'Rain';
    windSpeed: number;
  };
  forecast: Forecast[];
}

interface WeatherBlockProps {
  location: string;
  locationData: WeatherData;
}

const WeatherBlock: React.FC<WeatherBlockProps> = ({ location, locationData }) => {
  return (
    <div className="weather-block">
      <h2 className="text-center mb-4">Weather Data for {location}</h2>
      <div className="current-weather">
        <h3>Current Weather</h3>
        <p>Temperature: {locationData.current.temperature}°C</p>
        <p>Condition: {locationData.current.condition}</p>
        <p>Wind Speed: {locationData.current.windSpeed} km/h</p>
      </div>
      {locationData.forecast.length > 0 ? (
        <div className="forecast-weather">
          <h3>Forecast</h3>
          <table className="table table-hover">
            <thead className="thead-dark">
              <tr>
                <th>Timestamp</th>
                <th>Temperature</th>
                <th>Precipitation</th>
                <th>Wind Speed</th>
                <th>Condition</th>
              </tr>
            </thead>
            <tbody>
              {locationData.forecast.map((item) => (
                <tr key={item.id}>
                  <td>{new Date(item.timestamp).toLocaleString()}</td>
                  <td>{item.temperature}°C</td>
                  <td>{item.precipitation ? item.precipitation + ' mm' : 'N/A'}</td>
                  <td>{item.wind_speed ? item.wind_speed + ' km/h' : 'N/A'}</td>
                  <td>{item.weatherCondition}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div>No forecast data available.</div>
      )}
    </div>
  );
};

export default WeatherBlock;
