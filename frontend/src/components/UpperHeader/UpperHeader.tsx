import React from 'react';
import LocationDisplay from '../LocationDisplay/LocationDisplay';
import './UpperHeader.css';

interface UpperHeaderProps {
  onLocationUpdate: (entityName: string, latitude: number, longitude: number) => void;
}

const UpperHeader: React.FC<UpperHeaderProps> = ({ onLocationUpdate }) => {
  return (
    <div className="upper-header">
      <LocationDisplay onLocationUpdate={onLocationUpdate} />
    </div>
  );
};

export default UpperHeader;
