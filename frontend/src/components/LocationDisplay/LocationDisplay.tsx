import React, { useEffect, useState, useCallback } from 'react';
import { fetchNearestPlace } from '../../services/apiServiceGeography'; // Adjust the path as needed
import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet';
import 'bootstrap/dist/css/bootstrap.min.css';
import './LocationDisplay.css';
import LocationRequestModal from '../LocationRequestModal/LocationRequestModal';

interface LocationDisplayProps {
  onLocationUpdate: (entityName: string, latitude: number, longitude: number) => void;
}

const LocationDisplay: React.FC<LocationDisplayProps> = ({ onLocationUpdate }) => {
  const { t } = useTranslation('LocationDisplay');
  const [entityName, setEntityName] = useState<string>(t('locating'));
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);
  const [fetchError, setFetchError] = useState<boolean>(false);
  const [showModal, setShowModal] = useState<boolean>(false);

  const handleClose = () => {
    setShowModal(false);
    localStorage.setItem('locationModalShown', 'true');
  };

  const handleAllow = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;
          setLatitude(lat);
          setLongitude(lon);
          checkAndFetchEntityData(lat, lon);
          localStorage.setItem('locationConsent', 'true');
          localStorage.setItem('latitude', lat.toString());
          localStorage.setItem('longitude', lon.toString());
          setShowModal(false);
        },
        (error) => {
          setEntityName(t('geolocation_not_supported'));
          setFetchError(true);
        }
      );
    }
  };

  const fetchEntityData = useCallback(async (latitude: number, longitude: number) => {
    try {
      const place = await fetchNearestPlace(latitude, longitude);
      setEntityName(place.name);
      setFetchError(false);
      onLocationUpdate(place.name, latitude, longitude);
      localStorage.setItem('entityName', place.name);
    } catch (error) {
      setEntityName(t('failed_to_fetch_entity'));
      setFetchError(true);
    }
  }, [onLocationUpdate, t]);

  const checkAndFetchEntityData = useCallback((latitude: number, longitude: number) => {
    const storedLatitude = localStorage.getItem('latitude');
    const storedLongitude = localStorage.getItem('longitude');
    const storedEntityName = localStorage.getItem('entityName');

    if (
      storedLatitude &&
      storedLongitude &&
      storedEntityName &&
      Number(storedLatitude) === latitude &&
      Number(storedLongitude) === longitude
    ) {
      setEntityName(storedEntityName);
      setFetchError(false);
      onLocationUpdate(storedEntityName, latitude, longitude);
    } else {
      fetchEntityData(latitude, longitude);
    }
  }, [fetchEntityData, onLocationUpdate]);

  useEffect(() => {
    const storedConsent = localStorage.getItem('locationConsent');
    const storedLatitude = localStorage.getItem('latitude');
    const storedLongitude = localStorage.getItem('longitude');
    const storedEntityName = localStorage.getItem('entityName');

    if (storedConsent && storedLatitude && storedLongitude && storedEntityName) {
      const lat = Number(storedLatitude);
      const lon = Number(storedLongitude);
      setLatitude(lat);
      setLongitude(lon);
      setEntityName(storedEntityName);
      setFetchError(false);
      onLocationUpdate(storedEntityName, lat, lon);
    } else {
      const modalShown = localStorage.getItem('locationModalShown');
      if (!modalShown) {
        setShowModal(true);
      }
    }
  }, [checkAndFetchEntityData, t, onLocationUpdate]);

  return (
    <div className="location-display-container">
      <Helmet>
        <title>{t('appTitle')} - {entityName}</title>
        <meta name="description" content={`${t('current_location')}: ${entityName}, ${t('coordinates')}: ${latitude}, ${longitude}`} />
        <meta name="keywords" content="Kairos, Location, Coordinates, Geolocation, React" />
      </Helmet>
      {showModal && <LocationRequestModal show={showModal} handleClose={handleClose} handleAllow={handleAllow} />}

      <div className="location-content">
        <div className="location-info">
          <div className="single-line">
            <span className={`dot ${fetchError ? 'dot-red' : 'dot-green'}`}></span>
            <span className="entity-name">{entityName}</span>
          </div>
          {latitude !== null && longitude !== null && (
            <div className="coords">
              Lon: {longitude.toFixed(6)}, Lat: {latitude.toFixed(6)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LocationDisplay;
