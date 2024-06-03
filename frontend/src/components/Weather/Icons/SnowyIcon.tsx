import React from 'react';
import './SnowyIcon.css';

const SnowyIcon: React.FC<{ width?: number; height?: number; color?: string }> = ({ width = 100, height = 100, color = 'white' }) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 64 64"
      fill={color}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Replace this comment with the actual SVG path for the snowy icon */}
      <circle cx="32" cy="32" r="20" />
    </svg>
  );
};

export default SnowyIcon;
