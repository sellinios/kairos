import React from 'react';
import { WeatherSvg } from 'weather-icons-animated';
import { WeatherState } from './Wtypes';

interface WeatherIconProps {
  state: WeatherState;
  width?: number;
  height?: number;
  night?: boolean;
}

const WeatherIcon: React.FC<WeatherIconProps> = ({ state, width = 100, height = 100, night = false }) => {
  return <WeatherSvg state={state} width={width} height={height} night={night} />;
};

export default WeatherIcon;
