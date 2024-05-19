import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet';
import 'bootstrap/dist/css/bootstrap.min.css';
import './LocationDisplay.css';
import LocationRequestModal from '../LocationRequestModal/LocationRequestModal';

interface LocationDisplayProps {
  onLocationUpdate: (entityName: string, latitude: number, longitude: number) => void;
}

const LocationDisplay: React.FC<LocationDisplayProps> = ({ onLocationUpdate }) => {
  const { t } = useTranslation('LocationDisplay'); // Specify the namespace
  const [entityName, setEntityName] = useState<string>(t('locating'));
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);
  const [fetchError, setFetchError] = useState<boolean>(false);
  const [showModal, setShowModal] = useState<boolean>(true);

  const handleClose = () => setShowModal(false);

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
      const response = await axios.get('/api/places/entity-name/', {
        params: { latitude, longitude }
      });

      if (response.data.entity_name) {
        setEntityName(response.data.entity_name);
        setFetchError(false);
        onLocationUpdate(response.data.entity_name, latitude, longitude);
        localStorage.setItem('entityName', response.data.entity_name);
      } else {
        setEntityName(t('entity_not_found'));
        onLocationUpdate('Unknown Entity', latitude, longitude);
      }
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
      setShowModal(true);
    }
  }, [checkAndFetchEntityData, t, onLocationUpdate]);

  return (
    <div className="location-display">
      <Helmet>
        <title>{t('appTitle')} - {entityName}</title>
        <meta name="description" content={`${t('current_location')}: ${entityName}, ${t('coordinates')}: ${latitude}, ${longitude}`} />
        <meta name="keywords" content="Kairos, Location, Coordinates, Geolocation, React" />
      </Helmet>
      {showModal && <LocationRequestModal show={showModal} handleClose={handleClose} handleAllow={handleAllow} />}
      <div className="location-info">
        <div className="first-line">
          <span className={`dot ${fetchError ? 'dot-red' : 'dot-green'}`}></span>
          <span className="entity-name">{entityName}</span>
        </div>
        {(latitude !== null && longitude !== null) && (
          <div className="second-line">
            <span className="coords">{latitude.toFixed(6)}, {longitude.toFixed(6)}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default LocationDisplay;
