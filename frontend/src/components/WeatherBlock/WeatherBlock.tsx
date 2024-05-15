import React from 'react';
import './WeatherBlock.css';
import clearDayIcon from '../../assets/icons/clear-day.svg';
import partlyCloudyIcon from '../../assets/icons/partly-cloudy-day.svg';
import rainIcon from '../../assets/icons/rain.svg';
import windIcon from '../../assets/icons/wind.svg';

interface Forecast {
  day: string;
  temperature: number;
  weatherCondition: string;
  weatherIcon: string;
}

interface WeatherBlockProps {
  location: string;
  locationData: {
    current?: {
      temperature: number;
      condition: string;
      windSpeed: number;
    };
    forecast?: Forecast[];
  };
}

const WeatherBlock: React.FC<WeatherBlockProps> = ({ location, locationData }) => {
  const weatherData = {
    location: location,
    current: {
      temperature: locationData?.current?.temperature || 22,
      weatherCondition: locationData?.current?.condition || 'Clear Day',
      weatherIcon: clearDayIcon,
      windSpeed: locationData?.current?.windSpeed || 15,
      windIcon: windIcon,
    },
    forecast: locationData?.forecast || [
      { day: "Tomorrow", temperature: 20, weatherCondition: "Partly Cloudy", weatherIcon: partlyCloudyIcon },
      { day: "Wednesday", temperature: 18, weatherCondition: "Rain", weatherIcon: rainIcon },
      { day: "Thursday", temperature: 21, weatherCondition: "Clear Day", weatherIcon: clearDayIcon },
    ],
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Weather in {weatherData.location}</h2>
      <div className="card mb-3">
        <div className="card-body">
          <h5 className="card-title">Current Weather</h5>
          <p className="card-text">
            <img src={weatherData.current.weatherIcon} alt={weatherData.current.weatherCondition} width="50" />
            <strong>{weatherData.current.temperature}°C</strong> - {weatherData.current.weatherCondition}
          </p>
          <p className="card-text">
            <img src={weatherData.current.windIcon} alt="Wind" width="50" />
            Wind Speed: {weatherData.current.windSpeed} km/h
          </p>
        </div>
      </div>
      <table className="table table-hover">
        <thead className="thead-dark">
          <tr>
            <th>Day</th>
            <th>Condition</th>
            <th>Temperature</th>
          </tr>
        </thead>
        <tbody>
          {weatherData.forecast.map((forecast: Forecast, index: number) => (
            <tr key={index}>
              <td>{forecast.day}</td>
              <td>
                <img src={forecast.weatherIcon} alt={forecast.weatherCondition} width="30" /> {forecast.weatherCondition}
              </td>
              <td>{forecast.temperature}°C</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default WeatherBlock;