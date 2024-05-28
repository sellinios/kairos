// Explicitly re-export the Place interface with aliasing to avoid conflicts
export type { Place as GeographyPlace } from './apiServiceGeography';
export type { WeatherPlace } from './apiServiceWeather'; // Use the correct exported type

export * from './apiServiceArticles';
export * from './apiServiceGeography';
export * from './apiServiceWeather';
