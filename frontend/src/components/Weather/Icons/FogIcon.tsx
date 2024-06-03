import React from 'react';
import './FogIcon.css';

const FogIcon: React.FC<{ width?: number; height?: number; color?: string }> = ({ width = 100, height = 100, color = 'lightgray' }) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 64 64"
      fill={color}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Replace this comment with the actual SVG path for the fog icon */}
      <circle cx="32" cy="32" r="20" />
    </svg>
  );
};

export default FogIcon;
