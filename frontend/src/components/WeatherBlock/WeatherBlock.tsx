import React from 'react';
import './WeatherBlock.css';
import clearDayIcon from '../../assets/icons/clear-day.svg';
import partlyCloudyIcon from '../../assets/icons/partly-cloudy-day.svg';
import rainIcon from '../../assets/icons/rain.svg';
import windIcon from '../../assets/icons/wind.svg';

// Define WeatherCondition type
type WeatherCondition = 'Clear Day' | 'Partly Cloudy' | 'Rain';

// Define getWeatherIcon function
const getWeatherIcon = (condition: WeatherCondition): string => {
  switch (condition) {
    case 'Clear Day':
      return clearDayIcon;
    case 'Partly Cloudy':
      return partlyCloudyIcon;
    case 'Rain':
      return rainIcon;
    default:
      return clearDayIcon;
  }
};

interface Forecast {
  day: string;
  temperature: number;
  weatherCondition: WeatherCondition;
}

interface WeatherBlockProps {
  location: string;
  locationData?: {
    current?: {
      temperature: number;
      condition: WeatherCondition;
      windSpeed: number;
    };
    forecast?: Forecast[];
  } | null;
}

const WeatherBlock: React.FC<WeatherBlockProps> = ({ location, locationData }) => {
  console.log('WeatherBlock locationData:', locationData);

  if (!locationData) {
    return <div>Loading...</div>;
  }

  const { current, forecast } = locationData;

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Weather in {location}</h2>
      {current ? (
        <div className="card mb-3">
          <div className="card-body">
            <h5 className="card-title">Current Weather</h5>
            <p className="card-text">
              <img src={windIcon} alt="Wind icon" width="50" />
              Wind Speed: {current.windSpeed} km/h
            </p>
            <p className="card-text">
              <img src={getWeatherIcon(current.condition)} alt={current.condition} width="50" />
              <strong>{current.temperature}°C</strong> - {current.condition}
            </p>
          </div>
        </div>
      ) : (
        <div>No current weather data available.</div>
      )}
      {forecast && forecast.length > 0 ? (
        <table className="table table-hover">
          <thead className="thead-dark">
            <tr>
              <th>Day</th>
              <th>Condition</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {forecast.map((item, index) => (
              <tr key={index}>
                <td>{item.day}</td>
                <td>
                  <img src={getWeatherIcon(item.weatherCondition)} alt={item.weatherCondition} width="30" />
                  {item.weatherCondition}
                </td>
                <td>{item.temperature}°C</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div>No forecast data available.</div>
      )}
    </div>
  );
};

export default WeatherBlock;
