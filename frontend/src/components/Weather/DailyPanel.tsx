import React, { useState } from 'react';
import WeatherIcon from './WeatherIcon';
import { DailyForecast } from './types';
import { WeatherState } from './Wtypes';
import './DailyPanel.css';
import TemperatureChart from './TemperatureChart';

const countryTimeZones: { [key: string]: string } = {
  'greece': 'Europe/Athens',
  'japan': 'Asia/Tokyo',
  // Add more countries and their time zones here as needed
};

interface DailyPanelProps {
  daily: DailyForecast;
  country: string;
}

const DailyPanel: React.FC<DailyPanelProps> = ({ daily, country }) => {
  const [showHourlyDetails, setShowHourlyDetails] = useState(false);

  const getGeneralTextDetails = (text: string): string => {
    return text;
  };

  const getCardinalDirection = (angle: number) => {
    const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    const index = Math.floor((angle / 22.5) + 0.5) % 16;
    return directions[index];
  };

  const roundCloudCover = (value: number) => {
    return Math.round(value);
  };

  const formatDateTime = (date: string, hour: number, country: string) => {
    const utcDate = new Date(`${date}T${hour.toString().padStart(2, '0')}:00:00Z`);
    const timeZone = country ? countryTimeZones[country.toLowerCase()] : 'UTC';
    const options: Intl.DateTimeFormatOptions = {
      timeZone: timeZone,
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    };
    return utcDate.toLocaleTimeString('en-GB', options);
  };

  const calculateTotalPrecipitation = () => {
    return daily.hourlyForecasts.reduce((total, forecast) => total + forecast.forecast_data.precipitation_rate_level_0_surface, 0);
  };

  const totalPrecipitation = calculateTotalPrecipitation();

  const getWeatherIconState = (description: string, cloudCover: number, precipitation: number): WeatherState => {
    if (precipitation > 0 || description.toLowerCase().includes('rain') || description.toLowerCase().includes('storm')) {
      return 'rainy';
    }

    if (description.toLowerCase().includes('snow')) {
      return 'snowy';
    }

    if (description.toLowerCase().includes('fog')) {
      return 'fog';
    }

    if (description.toLowerCase().includes('hail')) {
      return 'hail';
    }

    if (description.toLowerCase().includes('thunder')) {
      return 'lightning';
    }

    if (cloudCover < 25) {
      return description.toLowerCase().includes('night') ? 'clear-night' : 'sunny';
    } else if (cloudCover < 50) {
      return 'partlycloudy';
    } else if (cloudCover < 75) {
      return 'cloudy';
    } else {
      return 'cloudy';
    }
  };

  const generalIconState = getWeatherIconState(
    daily.generalText,
    daily.hourlyForecasts[0].forecast_data.high_cloud_cover_level_0_highCloudLayer,
    daily.hourlyForecasts[0].forecast_data.precipitation_rate_level_0_surface
  );

  const chartData = daily.hourlyForecasts.map(forecast => ({
    date: formatDateTime(forecast.date, forecast.hour, country),
    temperature: forecast.temperature_celsius,
  }));

  return (
    <div className="daily-panel bg-dark text-white">
      <div className="panel-header d-flex justify-content-between align-items-center">
        <div className="panel-date">{new Date(daily.date).toLocaleDateString()}</div>
        <div className="panel-icon">
          <WeatherIcon state={generalIconState} width={100} height={100} />
        </div>
        <div className="panel-temp">{`Max: ${daily.maxTemp.toFixed(1)}°C`}</div>
      </div>
      <TemperatureChart data={chartData} />
      <div className="panel-body">
        <div>{getGeneralTextDetails(daily.generalText)}</div>
        <div>{`Min: ${daily.minTemp.toFixed(1)}°C`}</div>
        <div>Wind: {daily.hourlyForecasts[0] && getCardinalDirection(daily.hourlyForecasts[0].wind_direction)} {daily.hourlyForecasts[0] && (daily.hourlyForecasts[0].wind_speed * 3.6).toFixed(1)} km/h</div>
        <div>Precipitation: {totalPrecipitation.toFixed(2)} mm</div>
        <div>Cloud Cover: {daily.hourlyForecasts[0] && roundCloudCover(daily.hourlyForecasts[0].forecast_data.high_cloud_cover_level_0_highCloudLayer)}%</div>
        <button onClick={() => setShowHourlyDetails(!showHourlyDetails)} className="link btn btn-light mt-2">
          <span>{showHourlyDetails ? 'Hide' : 'Show'} Hourly Details</span>
        </button>
        {showHourlyDetails && (
          <div className="forecast-details mt-2">
            {daily.hourlyForecasts.map((forecast, index) => (
              <div key={index} className="forecast-detail mb-2">
                <div>Time: {formatDateTime(forecast.date, forecast.hour, country)}</div>
                <div>Temp: {forecast.temperature_celsius.toFixed(1)}°C</div>
                <div>Wind: {getCardinalDirection(forecast.wind_direction)} {forecast.wind_speed.toFixed(1)} km/h</div>
                <div>Precipitation: {forecast.forecast_data.precipitation_rate_level_0_surface.toFixed(2)} mm</div>
                <div>Cloud Cover: {roundCloudCover(forecast.forecast_data.high_cloud_cover_level_0_highCloudLayer)}%</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DailyPanel;
