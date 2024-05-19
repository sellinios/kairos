import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import { Modal, Button } from 'react-bootstrap';

interface LocationRequestModalProps {
  show: boolean;
  handleClose: () => void;
  handleAllow: () => void;
}

const LocationRequestModal: React.FC<LocationRequestModalProps> = ({ show, handleClose, handleAllow }) => {
  const { t } = useTranslation('LocationRequestModal'); // Specify the namespace

  return (
    <>
      <Helmet>
        <title>{t('locationAccessTitle')} - Kairos</title>
        <meta name="description" content={t('locationAccessDescription')} />
        <meta name="keywords" content={t('locationAccessKeywords')} />
      </Helmet>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{t('locationAccessTitle')}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{t('locationAccessBody')}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            {t('deny')}
          </Button>
          <Button variant="primary" onClick={handleAllow}>
            {t('allow')}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default LocationRequestModal;
