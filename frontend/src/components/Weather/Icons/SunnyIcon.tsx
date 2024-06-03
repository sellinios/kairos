import React from 'react';
import './SunnyIcon.css';

interface SunnyIconProps {
  width?: number;
  height?: number;
  color?: string;
  className?: string; // Add className prop
}

const SunnyIcon: React.FC<SunnyIconProps> = ({ width = 100, height = 100, color = 'yellow', className }) => {
  return (
    <svg
      className={`rotate ${className}`} // Include className here
      width={width}
      height={height}
      viewBox="0 0 64 64"
      fill={color}
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle cx="32" cy="32" r="14" />
      <line x1="32" y1="2" x2="32" y2="16" stroke={color} strokeWidth="2" />
      <line x1="32" y1="48" x2="32" y2="62" stroke={color} strokeWidth="2" />
      <line x1="2" y1="32" x2="16" y2="32" stroke={color} strokeWidth="2" />
      <line x1="48" y1="32" x2="62" y2="32" stroke={color} strokeWidth="2" />
      <line x1="11" y1="11" x2="21" y2="21" stroke={color} strokeWidth="2" />
      <line x1="43" y1="43" x2="53" y2="53" stroke={color} strokeWidth="2" />
      <line x1="11" y1="53" x2="21" y2="43" stroke={color} strokeWidth="2" />
      <line x1="43" y1="21" x2="53" y2="11" stroke={color} strokeWidth="2" />
    </svg>
  );
};

export default SunnyIcon;
