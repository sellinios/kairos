import React from 'react';
import './RainyIcon.css';

interface RainyIconProps {
  width?: number;
  height?: number;
  color?: string;
  className?: string; // Add className prop
}

const RainyIcon: React.FC<RainyIconProps> = ({ width = 100, height = 100, color = 'blue', className }) => {
  return (
    <svg
      className={className} // Include className here
      width={width}
      height={height}
      viewBox="0 0 64 64"
      fill={color}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Replace this comment with the actual SVG path for the rainy icon */}
      <circle cx="32" cy="32" r="20" />
    </svg>
  );
};

export default RainyIcon;
