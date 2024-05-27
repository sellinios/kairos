import React from 'react';
import LocationDisplay from '../LocationDisplay/LocationDisplay';

interface UpperHeaderProps {
  onLocationUpdate?: (location: string, latitude: number, longitude: number) => void;
}

const UpperHeader: React.FC<UpperHeaderProps> = ({ onLocationUpdate = () => {} }) => {
  return (
    <div>
      {/* Your UpperHeader content */}
      <LocationDisplay onLocationUpdate={onLocationUpdate} />
    </div>
  );
};

export default UpperHeader;
