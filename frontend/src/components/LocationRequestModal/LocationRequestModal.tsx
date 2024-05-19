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
        <Modal.Title>Location Access</Modal.Title>
      </Modal.Header>
      <Modal.Body>We need to access your location to provide better service.</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Deny
        </Button>
        <Button variant="primary" onClick={handleAllow}>
          Allow
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default LocationRequestModal;
