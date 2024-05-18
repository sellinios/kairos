import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

const PlaceDetail = () => {
    const { placeName } = useParams();
    const [place, setPlace] = useState(null);
    const [forecast, setForecast] = useState(null);

    useEffect(() => {
        fetch(`/api/places/?name=${placeName}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    setPlace(data[0]);
                    fetch(`/api/places/${data[0].id}/forecast/`)
                        .then(response => response.json())
                        .then(setForecast);
                }
            });
    }, [placeName]);

    if (!place) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>{place.name}</h1>
            <p>Latitude: {place.latitude}</p>
            <p>Longitude: {place.longitude}</p>
            <Link to={`/weather/${placeName}`}>Check Weather</Link>
            {forecast && (
                <div>
                    <h2>Weather Forecast</h2>
                    <pre>{JSON.stringify(forecast, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default PlaceDetail;
