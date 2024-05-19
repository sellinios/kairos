import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import 'bootstrap/dist/css/bootstrap.min.css';
import './LocationDisplay.css';
import LocationRequestModal from '../LocationRequestModal/LocationRequestModal';

interface LocationDisplayProps {
  onLocationUpdate: (entityName: string, latitude: number, longitude: number) => void;
}

const LocationDisplay: React.FC<LocationDisplayProps> = ({ onLocationUpdate }) => {
  const { t } = useTranslation();
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
          console.log(`Geolocation successful: ${lat}, ${lon}`);
          setLatitude(lat);
          setLongitude(lon);
          checkAndFetchEntityData(lat, lon);
          localStorage.setItem('locationConsent', 'true');
          localStorage.setItem('latitude', lat.toString());
          localStorage.setItem('longitude', lon.toString());
          setShowModal(false);
        },
        (error) => {
          console.error('Geolocation error:', error);
          setEntityName(t('geolocation_not_supported'));
          setFetchError(true);
        }
      );
    }
  };

  const fetchEntityData = useCallback(async (latitude: number, longitude: number) => {
    try {
      console.log(`Fetching entity data for coordinates: ${latitude}, ${longitude}`);
      const response = await axios.get('/api/places/entity-name/', {
        params: { latitude, longitude }
      });

      if (response.data.entity_name) {
        console.log(`Entity found: ${response.data.entity_name}`);
        setEntityName(response.data.entity_name);
        setFetchError(false);
        onLocationUpdate(response.data.entity_name, latitude, longitude);
        localStorage.setItem('entityName', response.data.entity_name);  // Store entity name
      } else {
        console.warn('Entity not found in database');
        setEntityName(t('entity_not_found'));
        onLocationUpdate('Unknown Entity', latitude, longitude);
      }
    } catch (error) {
      console.error('Error fetching entity data from database:', error);
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
      console.log('Using stored entity name:', storedEntityName);
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
      console.log(`Using stored location: ${lat}, ${lon}`);
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
      {showModal && <LocationRequestModal show={showModal} handleClose={handleClose} handleAllow={handleAllow} />}
      <span className={`dot ${fetchError ? 'dot-red' : 'dot-green'}`}></span>
      <div className="location-info">
        <span className="font-weight-bold">{t('current_location')}:</span> {entityName}
        {(latitude !== null && longitude !== null) && (
          <>
            <span className="font-weight-bold">, {t('latitude')}:</span> {latitude.toFixed(6)}, <span className="font-weight-bold">{t('longitude')}:</span> {longitude.toFixed(6)}
          </>
        )}
      </div>
    </div>
  );
};

export default LocationDisplay;
