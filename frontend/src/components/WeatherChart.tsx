import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import { WeatherChartData } from '../types/weather';
import { Data, Layout } from 'plotly.js';

interface WeatherChartProps {
    data: WeatherChartData;
    city: string;
}

const WeatherChart: React.FC<WeatherChartProps> = ({ data, city }) => {
    const [activeTab, setActiveTab] = useState<'temperature' | 'humidity' | 'wind' | 'pressure'>('temperature');

    const temperatureData: Data[] = [{
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Temperature',
        x: data.dates,
        y: data.temperatures,
        line: { color: '#ef4444', width: 3 },
        marker: { size: 8, color: '#ef4444' },
        hovertemplate: '%{y}°C<extra></extra>'
    }];

    const humidityData: Data[] = [{
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Humidity',
        x: data.dates,
        y: data.humidity,
        line: { color: '#3b82f6', width: 3 },
        marker: { size: 8, color: '#3b82f6' },
        hovertemplate: '%{y}%<extra></extra>'
    }];

    const windData: Data[] = [{
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Wind Speed',
        x: data.dates,
        y: data.windSpeed,
        line: { color: '#10b981', width: 3 },
        marker: { size: 8, color: '#10b981' },
        hovertemplate: '%{y} m/s<extra></extra>'
    }];

    const pressureData: Data[] = [{
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Pressure',
        x: data.dates,
        y: data.pressure,
        line: { color: '#8b5cf6', width: 3 },
        marker: { size: 8, color: '#8b5cf6' },
        hovertemplate: '%{y} hPa<extra></extra>'
    }];

    const getActiveData = () => {
        switch (activeTab) {
            case 'temperature': return temperatureData;
            case 'humidity': return humidityData;
            case 'wind': return windData;
            case 'pressure': return pressureData;
        }
    };

    const layout: Partial<Layout> = {
        title: {
            text: `${activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Forecast for ${city}`,
            font: { size: 24, family: 'Inter, sans-serif' }
        },
        height: 400,
        margin: { t: 50, r: 50, b: 50, l: 50 },
        showlegend: false,
        xaxis: {
            title: { text: 'Date' },
            tickangle: -45,
            gridcolor: '#e5e7eb',
            zerolinecolor: '#e5e7eb'
        },
        yaxis: {
            title: { text: activeTab === 'temperature' ? 'Temperature (°C)' : 
                        activeTab === 'humidity' ? 'Humidity (%)' :
                        activeTab === 'wind' ? 'Wind Speed (m/s)' : 'Pressure (hPa)' },
            gridcolor: '#e5e7eb',
            zerolinecolor: '#e5e7eb'
        },
        paper_bgcolor: 'rgba(255,255,255,0.9)',
        plot_bgcolor: 'rgba(255,255,255,0.9)',
        hovermode: 'x unified' as const
    };

    return (
        <div className="bg-white/90 rounded-2xl shadow-lg p-6 border border-cyan-100 mb-6">
            <div className="flex justify-between items-center mb-6">
                <div className="text-xl font-bold text-blue-700">Weather Forecast Chart</div>
                <div className="flex gap-2">
                    {(['temperature', 'humidity', 'wind', 'pressure'] as const).map((tab) => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors
                                ${activeTab === tab 
                                    ? 'bg-blue-500 text-white' 
                                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                        >
                            {tab.charAt(0).toUpperCase() + tab.slice(1)}
                        </button>
                    ))}
                </div>
            </div>
            <Plot
                data={getActiveData()}
                layout={layout}
                config={{ 
                    responsive: true,
                    displayModeBar: true,
                    displaylogo: false,
                    modeBarButtonsToRemove: ['lasso2d', 'select2d']
                }}
                style={{ width: '100%' }}
            />
        </div>
    );
};

export default WeatherChart; 