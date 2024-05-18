import React from 'react';
import { Modal, Button } from 'react-bootstrap';

interface LocationRequestModalProps {
  show: boolean;
  handleClose: () => void;
  handleAllow: () => void;
}

const LocationRequestModal: React.FC<LocationRequestModalProps> = ({ show, handleClose, handleAllow }) => {
  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Request for Location Access</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        We would like to access your location to provide accurate weather updates and forecasts for your area. Your location data will not be stored or shared.
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Decline
        </Button>
        <Button variant="primary" onClick={handleAllow}>
          Allow
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default LocationRequestModal;
