import React from 'react';
import './CloudyIcon.css';

interface CloudyIconProps {
  width?: number;
  height?: number;
  color?: string;
  className?: string; // Add className prop
}

const CloudyIcon: React.FC<CloudyIconProps> = ({ width = 100, height = 100, color = 'gray', className }) => {
  return (
    <svg
      className={className} // Include className here
      width={width}
      height={height}
      viewBox="0 0 64 64"
      fill={color}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Replace this comment with the actual SVG path for the cloudy icon */}
      <circle cx="32" cy="32" r="20" />
    </svg>
  );
};

export default CloudyIcon;
