import React, { useEffect, useState } from 'react';

interface WeatherData {
    temperature: number;
    weather_description: string;
}

interface Place {
    id: number;
    name: string;
    longitude: number;
    latitude: number;
    elevation: number;
    category: { id: number; name: string };
    admin_division: { id: number; name: string; level: number; slug: string; parent: number | null };
    url: string;
    weather_url: string;
    weather?: WeatherData;
}

const WeatherPage: React.FC = () => {
    const [placesWithWeather, setPlacesWithWeather] = useState<Place[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    async function fetchPlacesWithWeather() {
        try {
            const response = await fetch('/api/combined_places_weather/');
            if (!response.ok) throw new Error('Failed to fetch combined places and weather data');
            const data: Place[] = await response.json();
            console.log('Fetched data:', data);  // Log fetched data
            return data;
        } catch (err) {
            setError('Error fetching combined places and weather data');
            console.error('Error fetching combined places and weather data:', err);
            return [];
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        const fetchData = async () => {
            const data = await fetchPlacesWithWeather();
            if (data.length === 0) {
                setError('No data found');
                return;
            }
            setPlacesWithWeather(data);
        };
        fetchData();
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div>
            {placesWithWeather.map((place) => (
                <div key={place.id}>
                    <h2>{place.admin_division.name}</h2>
                    <p>Longitude: {place.longitude}</p>
                    <p>Latitude: {place.latitude}</p>
                    {place.weather ? (
                        <>
                            <p>Weather: {place.weather.weather_description}</p>
                            <p>Temperature: {place.weather.temperature}°C</p>
                        </>
                    ) : (
                        <p>Weather data not available</p>
                    )}
                </div>
            ))}
        </div>
    );
};

export default WeatherPage;
