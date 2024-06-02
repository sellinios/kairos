export interface ForecastData {
    precipitation_rate_level_0_surface: number;
    low_cloud_cover_level_0_lowCloudLayer: number;
    temperature_level_2_heightAboveGround: number;
    high_cloud_cover_level_0_highCloudLayer: number;
    medium_cloud_cover_level_0_middleCloudLayer: number;
    u_component_of_wind_level_10_heightAboveGround: number;
    v_component_of_wind_level_10_heightAboveGround: number;
    total_precipitation_level_0_surface?: number;
    convective_precipitation_level_0_surface?: number;
    convective_precipitation_rate_level_0_surface?: number;
    maximum_temperature_level_2_heightAboveGround?: number;
    minimum_temperature_level_2_heightAboveGround?: number;
    convective_available_potential_energy_level_0_surface?: number;
}

export interface Forecast {
    id: number;
    latitude: number;
    longitude: number;
    temperature_celsius: number;
    wind_speed: number;
    wind_direction: number;
    forecast_data: ForecastData;
    date: string;
    hour: number;
}

export interface DailyForecast {
    date: string;
    minTemp: number;
    maxTemp: number;
    generalIcon: JSX.Element;
    generalText: string;
    hourlyForecasts: Forecast[];
}
