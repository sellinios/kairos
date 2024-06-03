import React from 'react';
import SunnyIcon from './Icons/SunnyIcon';
import { WeatherState } from './types';

interface WeatherIconProps {
  state: WeatherState;
  width?: number;
  height?: number;
  color?: string;
}

const WeatherIcon: React.FC<WeatherIconProps> = ({ state, width = 100, height = 100, color = 'orange' }) => {
  switch (state) {
    case 'sunny':
      return <SunnyIcon width={width} height={height} color={color} />;
    // Add cases for other weather states and their corresponding icons
    default:
      return null;
  }
};

export default WeatherIcon;
