import React, { useState } from 'react';
import { weatherService } from './services/weatherService';
import WeatherCard from './components/WeatherCard';
import WeatherTable from './components/WeatherTable';
import WeatherChart from './components/WeatherChart';
import { WeatherData, WeatherTableData, WeatherForecast } from './types/weather';
import SampleQueries from './components/SampleQueries';

function App() {
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
    const [tableData, setTableData] = useState<WeatherTableData[] | null>(null);
    const [textSummary, setTextSummary] = useState<string | null>(null);
    const [displayFormat, setDisplayFormat] = useState<'text' | 'table' | 'chart' | null>(null);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) {
            setError('Please enter a query or city name');
            return;
        }

        setLoading(true);
        setError(null);
        setWeatherData(null);
        setTableData(null);
        setTextSummary(null);
        setDisplayFormat(null);

        try {
            console.log('Sending query:', query);
            const result = await weatherService.analyzeWeather(query);
            console.log('Received result:', result);
            
            // Set the display format based on the response
            setDisplayFormat(result.format ?? null);
            
            if (result.text_summary) {
                setTextSummary(result.text_summary);
            }
            
            if (result.data && Array.isArray(result.data)) {
                // Map the data to the expected format
                const mappedData = result.data.map((item: WeatherForecast) => ({
                    date: item.date,
                    temperature: item.temperature,
                    humidity: item.humidity,
                    windSpeed: item.windSpeed,
                    pressure: item.pressure,
                    description: item.description,
                    icon: item.icon,
                    city: item.city
                }));
                
                setTableData(mappedData);
                setWeatherData({
                    city: result.data[0].city,
                    forecast: mappedData
                });
            }
        } catch (err) {
            console.error('Error in handleSearch:', err);
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    const forecast = weatherData?.forecast || [];

    // Find the forecast entry for today, or fallback to the first day
    let cardForecast = null;
    if (weatherData && weatherData.forecast && weatherData.forecast.length > 0) {
        const today = new Date();
        cardForecast = weatherData.forecast.find(f => {
            const forecastDate = new Date(f.date);
            return (
                forecastDate.getDate() === today.getDate() &&
                forecastDate.getMonth() === today.getMonth() &&
                forecastDate.getFullYear() === today.getFullYear()
            );
        }) || weatherData.forecast[0]; // fallback to first day if today not found
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-100 via-cyan-100 to-blue-200 font-sans">
            {/* AppBar as fixed header */}
            <header className="w-full bg-gradient-to-r from-blue-500 to-cyan-400 shadow-lg py-6 px-4 flex items-center justify-center fixed top-0 left-0 z-50">
                <div className="flex items-center space-x-4">
                    <span className="text-4xl text-yellow-200">☀️</span>
                    <div>
                        <h1 className="text-3xl md:text-4xl font-bold text-white tracking-wide">WeatherAI</h1>
                        <p className="text-cyan-100 text-sm md:text-base font-light mt-1">Your Smart Weather Forecasting Assistant</p>
                    </div>
                </div>
            </header>

            {/* Centered Search Section */}
            <div className="flex flex-col items-center justify-center min-h-[400px] w-full" style={{ paddingTop: '120px' }}>
                <div className="flex justify-center w-full">
                    <form onSubmit={handleSearch} className="w-full max-w-6xl bg-white/80 shadow-xl rounded-2xl p-8 backdrop-blur-md">
                        <div className="flex flex-col md:flex-row gap-4 items-center">
                            <input
                                type="text"
                                className="flex-1 px-5 py-3 rounded-lg border border-cyan-200 focus:ring-2 focus:ring-cyan-400 text-lg transition"
                                placeholder="e.g., Show me the temperature forecast for the next 3 days in Tokyo as a chart."
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                            />
                            <button
                                type="submit"
                                className="bg-gradient-to-r from-blue-500 to-cyan-400 text-white font-semibold px-8 py-3 rounded-lg shadow-md hover:from-blue-600 hover:to-cyan-500 transition text-lg"
                                disabled={loading}
                            >
                                {loading ? 'Loading...' : 'Search'}
                            </button>
                        </div>
                        {error && <div className="mt-4 text-red-600 text-base font-medium bg-red-100 rounded-lg px-4 py-2">{error}</div>}
                        {/* Sample Queries Section */}
                        <SampleQueries onSelect={(q) => setQuery(q)} />
                    </form>
                </div>
            </div>

            {/* Results */}
            <div className="w-full flex flex-col items-center justify-center px-4 py-8 gap-8">
                <div className="w-full max-w-6xl flex flex-col gap-8 items-center justify-center">

                    {/* Show all if no format specified */}
                    {(!displayFormat || displayFormat === null) && (
                        <>
                            {textSummary && (
                                <div className="w-full bg-cyan-50 border-l-4 border-cyan-400 text-cyan-900 p-6 rounded-lg shadow">
                                    <span className="font-semibold text-lg">{textSummary}</span>
                                </div>
                            )}
                            {cardForecast && (
                                <div className="w-full">
                                    <WeatherCard city={weatherData?.city || ''} currentWeather={cardForecast} />
                                </div>
                            )}
                            {weatherData && (
                                <div className="w-full">
                                    <WeatherChart data={{
                                        dates: forecast.map(f => new Date(f.date).toLocaleDateString()),
                                        temperatures: forecast.map(f => f.temperature),
                                        humidity: forecast.map(f => f.humidity),
                                        windSpeed: forecast.map(f => f.windSpeed),
                                        pressure: forecast.map(f => f.pressure),
                                    }} city={weatherData.city} />
                                </div>
                            )}
                            {tableData && (
                                <div className="w-full">
                                    <WeatherTable data={tableData} />
                                </div>
                            )}
                        </>
                    )}

                    {/* Show only the requested format */}
                    {displayFormat === 'text' && weatherData && weatherData.forecast && weatherData.forecast.length > 0 && (
                        <div className="w-full">
                            <WeatherCard city={weatherData.city} currentWeather={weatherData.forecast[0]} />
                        </div>
                    )}
                    {displayFormat === 'text' && textSummary && (
                        <div className="w-full bg-cyan-50 border-l-4 border-cyan-400 text-cyan-900 p-6 rounded-lg shadow">
                            <span className="font-semibold text-lg">{textSummary}</span>
                        </div>
                    )}
                    {displayFormat === 'chart' && weatherData && (
                        <div className="w-full">
                            <WeatherChart data={{
                                dates: forecast.map(f => new Date(f.date).toLocaleDateString()),
                                temperatures: forecast.map(f => f.temperature),
                                humidity: forecast.map(f => f.humidity),
                                windSpeed: forecast.map(f => f.windSpeed),
                                pressure: forecast.map(f => f.pressure),
                            }} city={weatherData.city} />
                        </div>
                    )}
                    {displayFormat === 'table' && tableData && (
                        <div className="w-full">
                            <WeatherTable data={tableData} />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default App;
