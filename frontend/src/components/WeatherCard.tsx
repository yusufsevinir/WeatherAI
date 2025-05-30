import React from 'react';
import { WeatherForecast } from '../types/weather';

interface WeatherCardProps {
    city: string;
    currentWeather: WeatherForecast;
}

const WeatherCard: React.FC<WeatherCardProps> = ({ city, currentWeather }) => {
    return (
        <div className="bg-white/80 rounded-2xl shadow-lg p-6 flex flex-col md:flex-row items-center gap-6 border border-cyan-100">
            <div className="flex flex-col items-center md:w-1/3">
                <img
                    src={`https://openweathermap.org/img/wn/${currentWeather.icon || '01d'}@2x.png`}
                    alt={currentWeather.description}
                    className="w-24 h-24 mb-2"
                />
                <div className="text-lg font-semibold text-cyan-700 capitalize">{currentWeather.description}</div>
            </div>
            <div className="flex-1 flex flex-col items-center md:items-start gap-2">
                <div className="text-3xl md:text-5xl font-bold text-blue-700">{currentWeather.temperature}°C</div>
                <div className="text-xl font-semibold text-gray-700 mb-2">{city}</div>
                <div className="flex flex-wrap gap-4 text-gray-600 text-base">
                    <div>Humidity: <span className="font-medium">{currentWeather.humidity}%</span></div>
                    <div>Wind: <span className="font-medium">{currentWeather.windSpeed} m/s</span></div>
                    <div>Pressure: <span className="font-medium">{currentWeather.pressure} hPa</span></div>
                </div>
            </div>
        </div>
    );
};

export default WeatherCard; 