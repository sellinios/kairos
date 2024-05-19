import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

interface Place {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

const PlaceDetail: React.FC = () => {
  const { t } = useTranslation();
  const { placeName } = useParams<{ placeName: string }>();
  const [place, setPlace] = useState<Place | null>(null);
  const [forecast, setForecast] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlaceData = async () => {
      try {
        const placeResponse = await axios.get(`/api/geography/places/?name=${placeName}`);
        if (placeResponse.data.length > 0) {
          setPlace(placeResponse.data[0]);
          const forecastResponse = await axios.get(`/api/geography/places/${placeResponse.data[0].id}/forecast/`);
          setForecast(forecastResponse.data);
        } else {
          setError(t('placeNotFound'));
        }
      } catch (error) {
        console.error('Error fetching place data:', error);
        setError(t('placeNotFound'));
      }
    };

    fetchPlaceData();
  }, [placeName, t]);

  if (error) {
    return <div>{error}</div>;
  }

  if (!place) {
    return <div>{t('loading')}</div>;
  }

  return (
    <div>
      <Helmet>
        <title>{place.name} - {t('placeDetailsTitle')} - Kairos</title>
        <meta name="description" content={`${t('placeDetailsDescription')} ${place.name}. ${t('latitude')}: ${place.latitude}, ${t('longitude')}: ${place.longitude}.`} />
        <meta name="keywords" content={`${place.name}, ${t('placeDetailsKeywords')}, Kairos`} />
      </Helmet>
      <h1>{place.name}</h1>
      <p>{t('latitude')}: {place.latitude}</p>
      <p>{t('longitude')}: {place.longitude}</p>
      <Link to={`/weather/${placeName}`}>{t('checkWeather')}</Link>
      {forecast && (
        <div>
          <h2>{t('weatherForecast')}</h2>
          <pre>{JSON.stringify(forecast, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default PlaceDetail;
