export interface WeatherForecast {
    date: string;
    temperature: number;
    humidity: number;
    windSpeed: number;
    pressure: number;
    description: string;
    icon: string;
    city: string;
}

export interface WeatherData {
    city: string;
    forecast: WeatherForecast[];
}

export interface WeatherChartData {
    dates: string[];
    temperatures: number[];
    humidity: number[];
    windSpeed: number[];
    pressure: number[];
}

export interface WeatherTableData {
    date: string;
    temperature: number;
    humidity: number;
    windSpeed: number;
    pressure: number;
    description: string;
}

export interface WeatherQueryResult {
    type: 'forecast' | 'historical' | 'current';
    days: number;
    sentiment: string;
    confidence: number;
} 