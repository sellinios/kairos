import React, { useMemo } from 'react';
import WeatherIcon from './WeatherIcon';
import { DailyForecast, WeatherState } from './types';
import './DailyPanel.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const countryTimeZones = {
  'greece': 'Europe/Athens',
  'japan': 'Asia/Tokyo',
};

interface DailyPanelProps {
  forecasts: DailyForecast[];
  country: string;
  showHeaders: boolean;
}

const DailyPanel: React.FC<DailyPanelProps> = ({ forecasts, country, showHeaders }) => {
  const getCardinalDirection = (angle: number): string => {
    const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    const index = Math.floor((angle / 22.5) + 0.5) % 16;
    return directions[index];
  };

  const roundCloudCover = (value: number): number => Math.round(value);

  const calculateTotalPrecipitation = (daily: DailyForecast): number =>
    daily.hourlyForecasts.reduce((total, { forecast_data }) => total + forecast_data.precipitation_rate_level_0_surface, 0);

  const getWeatherIconState = (description: string, cloudCover: number, precipitation: number): WeatherState => {
    if (precipitation > 0 || /rain|storm/.test(description.toLowerCase())) {
      return 'rainy';
    }
    if (/snow/.test(description.toLowerCase())) {
      return 'snowy';
    }
    if (/fog/.test(description.toLowerCase())) {
      return 'fog';
    }
    if (/hail/.test(description.toLowerCase())) {
      return 'hail';
    }
    if (/thunder/.test(description.toLowerCase())) {
      return 'lightning';
    }
    if (cloudCover < 25) {
      return /night/.test(description.toLowerCase()) ? 'clear-night' : 'sunny';
    }
    if (cloudCover < 50) {
      return 'partlycloudy';
    }
    return 'cloudy';
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const options: Intl.DateTimeFormatOptions = { weekday: 'long', month: 'long', day: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
  };

  return (
    <div className="daily-panel container">
      {forecasts.map(({ date, generalText, maxTemp, minTemp, hourlyForecasts }) => {
        const totalPrecipitation = useMemo(
          () => calculateTotalPrecipitation({ date, generalText, maxTemp, minTemp, hourlyForecasts }),
          [hourlyForecasts]
        );
        const generalIconState = useMemo(
          () =>
            getWeatherIconState(
              generalText,
              hourlyForecasts[0]?.forecast_data.high_cloud_cover_level_0_highCloudLayer,
              hourlyForecasts[0]?.forecast_data.precipitation_rate_level_0_surface
            ),
          [generalText, hourlyForecasts]
        );

        return (
          <div key={date} className="row mb-3 forecast-row">
            <div className="col-12">
              <div className="d-flex flex-wrap align-items-center forecast-details">
                <div className="col-md-2 col-sm-6 panel-date">{formatDate(date)}</div>
                <div className="col-md-1 col-sm-6 d-flex align-items-center justify-content-center">
                  <WeatherIcon state={generalIconState} width={60} height={60} />
                </div>
                <div className="col-md-2 col-sm-6 temperature">
                  <span className="max-temp">{maxTemp.toFixed(1)}°C</span> / <span className="min-temp">{minTemp.toFixed(1)}°C</span>
                </div>
                <div className="col-md-2 col-sm-6 wind-direction">
                  <span style={{ transform: `rotate(${hourlyForecasts[0]?.wind_direction}deg)` }}>↑</span>
                  {hourlyForecasts[0] && getCardinalDirection(hourlyForecasts[0].wind_direction)}{' '}
                  {hourlyForecasts[0] && (hourlyForecasts[0].wind_speed * 3.6).toFixed(1)} km/h
                </div>
                <div className="col-md-2 col-sm-6 precipitation">
                  <span className="precipitation-tag">Precipitation: {totalPrecipitation.toFixed(2)} mm</span>
                </div>
                <div className="col-md-2 col-sm-6 alerts">No alerts</div>
              </div>
              <hr />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default DailyPanel;
