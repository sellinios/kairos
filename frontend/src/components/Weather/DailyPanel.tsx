import React from 'react';
import WeatherIcon from './WeatherIcon';
import { DailyForecast, WeatherState } from './types';
import './DailyPanel.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const countryTimeZones: { [key: string]: string } = {
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

  const roundCloudCover = (value: number): number => {
    return Math.round(value);
  };

  const calculateTotalPrecipitation = (daily: DailyForecast): number => {
    return daily.hourlyForecasts.reduce((total, forecast) => total + forecast.forecast_data.precipitation_rate_level_0_surface, 0);
  };

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

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const options: Intl.DateTimeFormatOptions = { weekday: 'long', month: 'long', day: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
  };

  return (
    <div className="daily-panel container">
      {showHeaders && (
        <div className="row mb-3">
          <div className="col-12">
            <div className="panel-header d-flex justify-content-between align-items-center">
              <div className="col-md-2 col-sm-2"><strong>Date</strong></div>
              <div className="col-md-1 col-sm-1 icon-header"><strong>Icon</strong></div>
              <div className="col-md-2 col-sm-2"><strong>Temperatures</strong></div>
              <div className="col-md-2 col-sm-2"><strong>Winds</strong></div>
              <div className="col-md-2 col-sm-2"><strong>Precipitation</strong></div>
              <div className="col-md-2 col-sm-2"><strong>Alerts</strong></div>
              <div className="col-md-1 col-sm-1"></div>
            </div>
          </div>
        </div>
      )}

      {forecasts.map(daily => {
        const totalPrecipitation = calculateTotalPrecipitation(daily);
        const generalIconState: WeatherState = getWeatherIconState(
          daily.generalText,
          daily.hourlyForecasts[0].forecast_data.high_cloud_cover_level_0_highCloudLayer,
          daily.hourlyForecasts[0].forecast_data.precipitation_rate_level_0_surface
        );

        return (
          <div key={daily.date} className="row mb-3 forecast-row">
            <div className="col-12">
              <div className="d-flex flex-wrap align-items-center forecast-details">
                <div className="col-md-2 col-sm-6">
                  <div className="panel-date">{formatDate(daily.date)}</div>
                </div>
                <div className="col-md-1 col-sm-6 d-flex align-items-center justify-content-center">
                  <WeatherIcon state={generalIconState} width={60} height={60} />
                </div>
                <div className="col-md-2 col-sm-6">
                  <div className="temperature">
                    <span className="max-temp">{daily.maxTemp.toFixed(1)}°C</span> / <span className="min-temp">{daily.minTemp.toFixed(1)}°C</span>
                  </div>
                </div>
                <div className="col-md-2 col-sm-6">
                  <div>
                    <span className="wind-direction" style={{ transform: `rotate(${daily.hourlyForecasts[0].wind_direction}deg)` }}>↑</span>
                    {daily.hourlyForecasts[0] && getCardinalDirection(daily.hourlyForecasts[0].wind_direction)} {daily.hourlyForecasts[0] && (daily.hourlyForecasts[0].wind_speed * 3.6).toFixed(1)} km/h
                  </div>
                </div>
                <div className="col-md-2 col-sm-6">
                  <div>Precipitation: {totalPrecipitation.toFixed(2)} mm</div>
                  <div>Cloud Cover: {daily.hourlyForecasts[0] && roundCloudCover(daily.hourlyForecasts[0].forecast_data.high_cloud_cover_level_0_highCloudLayer)}%</div>
                </div>
                <div className="col-md-2 col-sm-6">
                  <div>No alerts</div> {/* Placeholder for alerts */}
                </div>
                <div className="col-md-1 col-sm-12 text-right">
                  <a href="#" className="link">Open hourly forecast &gt;</a>
                </div>
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
