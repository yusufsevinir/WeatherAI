import { WeatherData, WeatherChartData, WeatherTableData } from '../types/weather';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class WeatherService {
    async getWeatherData(city: string): Promise<WeatherData> {
        const response = await fetch(`${API_BASE_URL}/api/weather/forecast?city=${encodeURIComponent(city)}&days=7`);
        if (!response.ok) {
            throw new Error('Failed to fetch weather data');
        }
        const data = await response.json();
        // Map backend response to frontend WeatherData
        return {
            city: data.city,
            forecast: data.forecast.map((item: any) => ({
                date: item.date,
                temperature: item.temperature,
                humidity: item.humidity,
                windSpeed: item.windSpeed,
                pressure: item.pressure,
                description: item.description,
                icon: item.icon,
                city: item.city
            }))
        };
    }

    async getWeatherChart(city: string): Promise<WeatherChartData> {
        // Use the same forecast endpoint and map to chart data
        const response = await fetch(`${API_BASE_URL}/api/weather/forecast?city=${encodeURIComponent(city)}&days=7`);
        if (!response.ok) {
            throw new Error('Failed to fetch weather chart data');
        }
        const data = await response.json();
        const dates: string[] = [];
        const temperatures: number[] = [];
        const humidity: number[] = [];
        const windSpeed: number[] = [];
        const pressure: number[] = [];
        data.forecast.forEach((item: any) => {
            dates.push(item.date);
            temperatures.push(item.temperature);
            humidity.push(item.humidity);
            windSpeed.push(item.windSpeed);
            pressure.push(item.pressure);
        });
        return { dates, temperatures, humidity, windSpeed, pressure };
    }

    async getWeatherTable(city: string): Promise<WeatherTableData[]> {
        // Use the same forecast endpoint and map to table data
        const response = await fetch(`${API_BASE_URL}/api/weather/forecast?city=${encodeURIComponent(city)}&days=7`);
        if (!response.ok) {
            throw new Error('Failed to fetch weather table data');
        }
        const data = await response.json();
        return data.forecast.map((item: any) => ({
            date: item.date,
            temperature: item.temperature,
            humidity: item.humidity,
            windSpeed: item.windSpeed,
            pressure: item.pressure,
            description: item.description
        }));
    }

    async analyzeWeather(query: string) {
        const response = await fetch(`${API_BASE_URL}/api/weather/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        if (!response.ok) {
            throw new Error('Failed to analyze weather query');
        }
        return response.json();
    }

    async getHistoricalWeather(city: string, days: number = 7): Promise<WeatherData> {
        const response = await fetch(`${API_BASE_URL}/api/weather/historical?city=${encodeURIComponent(city)}&days=${days}`);
        if (!response.ok) {
            throw new Error('Failed to fetch historical weather data');
        }
        const data = await response.json();
        // Map backend response to frontend WeatherData
        return {
            city: city,
            forecast: data.map((item: any) => ({
                date: item.date,
                temperature: item.temperature,
                humidity: item.humidity,
                windSpeed: item.windSpeed,
                pressure: item.pressure,
                description: item.description,
                icon: item.icon,
                city: item.city
            }))
        };
    }

    async getSampleQueries(): Promise<string[]> {
        const response = await fetch(`${API_BASE_URL}/api/sample-queries`);
        if (!response.ok) {
            throw new Error('Failed to fetch sample queries');
        }
        return response.json();
    }
}

export const weatherService = new WeatherService(); 