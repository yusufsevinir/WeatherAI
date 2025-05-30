import React from 'react';
import { WeatherTableData } from '../types/weather';

interface WeatherTableProps {
    data: WeatherTableData[];
}

const WeatherTable: React.FC<WeatherTableProps> = ({ data }) => {
    const getWeatherIcon = (description: string) => {
        const desc = description.toLowerCase();
        if (desc.includes('clear')) return '☀️';
        if (desc.includes('cloud')) return '☁️';
        if (desc.includes('rain')) return '🌧️';
        if (desc.includes('snow')) return '❄️';
        if (desc.includes('thunder')) return '⛈️';
        if (desc.includes('fog') || desc.includes('mist')) return '🌫️';
        return '🌤️';
    };

    const getTemperatureColor = (temp: number) => {
        if (temp >= 30) return 'text-red-600';
        if (temp >= 25) return 'text-orange-500';
        if (temp >= 20) return 'text-yellow-500';
        if (temp >= 15) return 'text-green-500';
        if (temp >= 10) return 'text-blue-500';
        return 'text-cyan-500';
    };

    return (
        <div className="bg-white/90 rounded-2xl shadow-lg p-6 border border-cyan-100 overflow-x-auto">
            <div className="text-xl font-bold text-blue-700 mb-6">Detailed Weather Forecast</div>
            <div className="overflow-x-auto">
                <table className="min-w-full text-sm">
                    <thead>
                        <tr className="bg-gradient-to-r from-blue-500 to-cyan-400 text-white">
                            <th className="py-3 px-4 text-left rounded-l-lg">Date</th>
                            <th className="py-3 px-4 text-center">Weather</th>
                            <th className="py-3 px-4 text-right">Temperature</th>
                            <th className="py-3 px-4 text-right">Humidity</th>
                            <th className="py-3 px-4 text-right">Wind</th>
                            <th className="py-3 px-4 text-right rounded-r-lg">Pressure</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {data.map((row, index) => {
                            const date = new Date(row.date);
                            return (
                                <tr key={index} className="hover:bg-cyan-50 transition-colors">
                                    <td className="py-3 px-4 font-medium text-gray-700">
                                        {date.toLocaleDateString(undefined, {
                                            weekday: 'short',
                                            month: 'short',
                                            day: 'numeric'
                                        })}
                                    </td>
                                    <td className="py-3 px-4 text-center">
                                        <div className="flex items-center justify-center gap-2">
                                            <span className="text-xl">{getWeatherIcon(row.description)}</span>
                                            <span className="capitalize text-gray-600">{row.description}</span>
                                        </div>
                                    </td>
                                    <td className={`py-3 px-4 text-right font-medium ${getTemperatureColor(row.temperature)}`}>
                                        {row.temperature.toFixed(1)}°C
                                    </td>
                                    <td className="py-3 px-4 text-right text-gray-600">{row.humidity}%</td>
                                    <td className="py-3 px-4 text-right text-gray-600">{row.windSpeed} m/s</td>
                                    <td className="py-3 px-4 text-right text-gray-600">{row.pressure} hPa</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default WeatherTable; 