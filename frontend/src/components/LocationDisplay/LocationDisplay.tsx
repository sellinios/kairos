import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './LocationDisplay.css';

interface LocationDisplayProps {
  location: string;
}

const LocationDisplay: React.FC<LocationDisplayProps> = ({ location }) => {
  return (
    <div className="location-display">
      <span className="font-weight-bold">Current Location:</span> {location}
    </div>
  );
}

export default LocationDisplay;
