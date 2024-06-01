import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './WeatherPage.css';
import RainIcon from '../../../assets/icons/extreme-day-rain.svg';
import CloudIcon from '../../../assets/icons/partly-cloudy-day.svg';
import SunIcon from '../../../assets/icons/clear-day.svg';

interface ForecastData {
    pressure_level_0_surface: number;
    temperature_level_2_heightAboveGround: number;
    wind_speed_gust_level_0_surface: number;
    precipitation_rate_level_0_surface: number;
    total_precipitation_level_0_surface?: number;
    low_cloud_cover_level_0_lowCloudLayer: number;
    high_cloud_cover_level_0_highCloudLayer: number;
    convective_precipitation_level_0_surface?: number;
    medium_cloud_cover_level_0_middleCloudLayer: number;
    convective_precipitation_rate_level_0_surface?: number;
    maximum_temperature_level_2_heightAboveGround?: number;
    minimum_temperature_level_2_heightAboveGround?: number;
    u_component_of_wind_level_10_heightAboveGround: number;
    v_component_of_wind_level_10_heightAboveGround: number;
    convective_available_potential_energy_level_0_surface: number;
}

interface Forecast {
    id: number;
    latitude: number;
    longitude: number;
    temperature_celsius: number;
    wind_speed: number;
    wind_direction: number;
    forecast_data: ForecastData;
    timestamp: string;
}

const WeatherPage: React.FC = () => {
    const { continent, country, region, subregion, city } = useParams<{
        continent: string;
        country: string;
        region: string;
        subregion: string;
        city: string;
    }>();
    const [forecasts, setForecasts] = useState<Forecast[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    async function fetchWeatherData() {
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
            console.log('Fetched data:', data);
            setForecasts(data);
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
    }

    useEffect(() => {
        fetchWeatherData();
    }, [continent, country, region, subregion, city]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    const formatDate = (timestamp: string) => {
        const date = new Date(timestamp);
        return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    };

    const getWeatherIcon = (precipitation: number, cloudCover: number) => {
        if (precipitation > 0) {
            return RainIcon;
        } else if (cloudCover > 50) {
            return CloudIcon;
        } else {
            return SunIcon;
        }
    };

    const roundCloudCover = (value: number) => {
        return Math.round(value);
    };

    const getCardinalDirection = (angle: number) => {
        const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
        const index = Math.floor((angle / 22.5) + 0.5) % 16;
        return directions[index];
    };

    return (
        <div className="weather-page">
            <h2>Weather for {city}</h2>
            {forecasts.length > 0 ? (
                <table className="weather-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Precipitation (mm/hr)</th>
                            <th>Conditions</th>
                            <th>Clouds (L/M/H)</th>
                            <th>Temperature (°C)</th>
                            <th>Wind Direction</th>
                            <th>Wind Speed (m/s)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {forecasts.map((forecast) => (
                            <tr key={forecast.id}>
                                <td>{formatDate(forecast.timestamp)}</td>
                                <td>{forecast.forecast_data.precipitation_rate_level_0_surface}</td>
                                <td>
                                    <img
                                        src={getWeatherIcon(
                                            forecast.forecast_data.precipitation_rate_level_0_surface,
                                            forecast.forecast_data.high_cloud_cover_level_0_highCloudLayer
                                        )}
                                        alt="weather icon"
                                    />
                                </td>
                                <td>
                                    {`${roundCloudCover(forecast.forecast_data.low_cloud_cover_level_0_lowCloudLayer)}/
                                      ${roundCloudCover(forecast.forecast_data.medium_cloud_cover_level_0_middleCloudLayer)}/
                                      ${roundCloudCover(forecast.forecast_data.high_cloud_cover_level_0_highCloudLayer)}`}
                                </td>
                                <td>{forecast.temperature_celsius.toFixed(2)}</td>
                                <td>{getCardinalDirection(forecast.wind_direction)}</td>
                                <td>{forecast.wind_speed.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No weather data available.</p>
            )}
        </div>
    );
};

export default WeatherPage;
