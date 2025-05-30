from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.models.weather import WeatherResponse, ForecastRequest, AnalysisResponse, WeatherData
from app.utils.nlp_parser import parse_query
from app.utils.data_loader import get_location_data
from app.utils.forecasting import generate_forecast
from meteostat import Point, Daily
import logging
import pandas as pd
import os
from app.utils.open_weather_api import OpenWeatherAPI

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        print("\n=== Initializing Weather Service ===")
        self.csv_path = os.path.join('data', 'weather', 'capital_cities_weather.csv')
        print(f"CSV path: {self.csv_path}")
        self._load_capital_cities_data()
        print("===================================\n")
        
    def _load_capital_cities_data(self):
        """Load the capital cities weather data from CSV"""
        try:
            print("\n=== Loading Capital Cities Data ===")
            print(f"Attempting to load from: {self.csv_path}")
            self.capital_cities_data = pd.read_csv(self.csv_path)
            print(f"Successfully loaded capital cities data")
            print(f"Total rows: {len(self.capital_cities_data)}")
            print(f"Columns: {self.capital_cities_data.columns.tolist()}")
            print(f"Sample data:\n{self.capital_cities_data.head(2)}")
            print("================================\n")
            logger.info(f"Successfully loaded capital cities weather data with {len(self.capital_cities_data)} rows")
        except Exception as e:
            print(f"ERROR loading capital cities data: {str(e)}")
            logger.error(f"Error loading capital cities weather data: {e}")
            self.capital_cities_data = pd.DataFrame()
            
    def _get_city_data(self, city: str, start_date: Optional[str] = None, end_date: Optional[str] = None, days: Optional[int] = None) -> pd.DataFrame:
        """Get weather data for a specific city from the capital cities dataset"""
        try:
            print(f"\n=== Searching for City Data ===")
            print(f"City: {city}")
            
            # Create a copy of the filtered data to avoid SettingWithCopyWarning
            city_data = self.capital_cities_data[self.capital_cities_data['city'].str.lower() == city.lower()].copy()
            
            print(f"Found {len(city_data)} rows for {city}")
            
            if city_data.empty:
                print("No data found for this city")
                return pd.DataFrame()
                
            # Convert time column to datetime using loc
            city_data.loc[:, 'date'] = pd.to_datetime(city_data['time'])
            
            # Set default date range to last 7 days if not specified
            if not end_date:
                end_date = pd.Timestamp.now()
            else:
                end_date = pd.to_datetime(end_date)
                
            if not start_date:
                if days:
                    start_date = end_date - pd.Timedelta(days=days)
                else:
                    start_date = end_date - pd.Timedelta(days=7)
            else:
                start_date = pd.to_datetime(start_date)
            
            print(f"Filtering data from {start_date} to {end_date}")
            
            # Filter by date range
            city_data = city_data[
                (city_data['date'] >= start_date) & 
                (city_data['date'] <= end_date)
            ]
            
            print(f"After date filtering: {len(city_data)} rows")
            print(f"Final data sample:\n{city_data.head(2)}")
            print("==============================\n")
            return city_data
        except Exception as e:
            print(f"Error in _get_city_data: {str(e)}")
            logger.error(f"Error getting city data: {e}")
            return pd.DataFrame()
        
    def _get_weather_icon(self, description: str) -> str:
        """Map weather description to icon code"""
        description = description.lower()
        if 'clear' in description:
            return '01d'
        elif 'sunny' in description:
            return '01d'
        elif 'partly cloudy' in description:
            return '02d'
        elif 'cloudy' in description:
            return '04d'
        elif 'rain' in description:
            return '10d'
        elif 'thunder' in description:
            return '11d'
        elif 'snow' in description:
            return '13d'
        elif 'mist' in description or 'fog' in description:
            return '50d'
        else:
            return '01d'  # default to clear sky
            
    def _convert_to_weather_data(self, data: Dict[str, Any], city: str) -> WeatherData:
        """Convert raw data to WeatherData model"""
        try:
            print(f"\n=== Converting Weather Data ===")
            print(f"Input data: {data}")
            
            # Map column names to expected format
            date_str = data.get('date', data.get('time', data.get('Date', data.get('Time'))))
            temp = data.get('temperature', data.get('Temperature', data.get('TEMP')))
            humidity = data.get('humidity', data.get('Humidity', data.get('HUM')))
            wind = data.get('wind_speed', data.get('WindSpeed', data.get('WIND')))
            pressure = data.get('pressure', data.get('Pressure', data.get('PRES')))
            description = data.get('description', data.get('Description', data.get('DESC', 'Clear')))
            
            print(f"Extracted values:")
            print(f"Date: {date_str}")
            print(f"Temperature: {temp}")
            print(f"Humidity: {humidity}")
            print(f"Wind: {wind}")
            print(f"Pressure: {pressure}")
            print(f"Description: {description}")
            
            # Convert date string to datetime
            if isinstance(date_str, (str, pd.Timestamp)):
                date = pd.to_datetime(date_str)
            else:
                date = date_str
                
            weather_data = WeatherData(
                date=date,
                temperature=float(temp) if temp is not None else 0.0,
                humidity=float(humidity) if humidity is not None else 0.0,
                windSpeed=float(wind) if wind is not None else 0.0,
                pressure=float(pressure) if pressure is not None else 1013.25,
                description=str(description),
                city=city,
                icon=self._get_weather_icon(str(description))
            )
            print(f"Converted WeatherData: {weather_data}")
            print("==============================\n")
            return weather_data
        except Exception as e:
            print(f"Error in _convert_to_weather_data: {str(e)}")
            logger.error(f"Error converting data to WeatherData: {e}")
            logger.error(f"Input data: {data}")
            raise
            
    async def get_historical_data(
        self,
        city: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        days: Optional[int] = None
    ) -> List[WeatherData]:
        """
        Get historical weather data for a specific city from the capital cities dataset.
        Falls back to Meteostat if data is not available in the CSV.
        """
        try:
            print(f"\n=== Getting Historical Data ===")
            print(f"City: {city}")
            print(f"Date range: {start_date} to {end_date}")
            print(f"Days: {days}")
            
            # Try to get data from capital cities CSV first
            city_data = self._get_city_data(city, start_date, end_date, days)
            
            if not city_data.empty:
                print(f"Found {len(city_data)} rows in capital cities dataset")
                result = [
                    self._convert_to_weather_data(record, city)
                    for record in city_data.to_dict('records')
                ]
                print(f"Returning {len(result)} WeatherData objects")
                return result
            
            print("No data found in capital cities dataset, falling back to Meteostat")
            
            # If no data in CSV, fall back to Meteostat
            # Get location data
            location_data = get_location_data(city)
            if not location_data:
                raise ValueError(f"Location {city} not found in our database")
                
            # Set default dates if not provided
            if not end_date:
                end_date = datetime.now()
            else:
                end_date = pd.to_datetime(end_date)
                
            if not start_date:
                if days:
                    start_date = end_date - timedelta(days=days)
                else:
                    start_date = end_date - timedelta(days=7)
            else:
                start_date = pd.to_datetime(start_date)
                
            # Create Point object for the city
            location = Point(location_data['latitude'], location_data['longitude'])
            
            # Get daily weather data
            data = Daily(location, start_date, end_date)
            data = data.fetch()
            
            if data.empty:
                raise ValueError(f"No historical data found for {city}")
            
            # Reset index to make date a column
            data = data.reset_index()
            
            # Add city name
            data['city'] = city
            
            # Rename columns to match our format
            data = data.rename(columns={
                'date': 'date',
                'tavg': 'temperature',
                'tmin': 'min_temperature',
                'tmax': 'max_temperature',
                'prcp': 'precipitation',
                'snow': 'snow',
                'wdir': 'wind_direction',
                'wspd': 'wind_speed',
                'wpgt': 'wind_gust',
                'pres': 'pressure',
                'tsun': 'sunshine'
            })
            
            logger.info(f"Retrieved {len(data)} rows of historical data from Meteostat")
            
            # Convert to WeatherData objects
            result = [
                self._convert_to_weather_data(record, city)
                for record in data.to_dict('records')
            ]
            
            print("==============================\n")
            return result
        except Exception as e:
            print(f"Error in get_historical_data: {str(e)}")
            logger.error(f"Error getting historical data: {str(e)}")
            raise Exception(f"Error getting historical data: {str(e)}")
                
    async def analyze_weather(self, query: str) -> AnalysisResponse:
        """Analyze weather data based on natural language query"""
        try:
            print(f"\n=== Analyzing Weather Query ===")
            print(f"Query: {query}")
            
            # Parse the query
            parsed = parse_query(query)
            print(f"Parsed query: {parsed}")
            
            if not parsed:
                print("ERROR: Failed to parse query")
                raise ValueError("Failed to parse query")
            
            # Get location data
            location = parsed.get('location')
            print(f"Location from query: {location}")
            
            if not location:
                print("ERROR: No location specified in query")
                raise ValueError("No location specified in query")
            
            # Get historical data
            days = parsed.get('duration', 7)
            print(f"Getting {days} days of historical data")
            
            weather_data = await self.get_historical_data(
                city=location,
                days=days
            )
            
            if not weather_data:
                print("ERROR: No weather data found")
                raise ValueError(f"No weather data found for {location}")
            
            print(f"Retrieved {len(weather_data)} days of weather data")
            
            # Create response
            response = WeatherResponse(
                location=location,
                data=weather_data,
                forecast=weather_data,
                city=location,
                generated_at=datetime.now()
            )
            
            # Generate summary
            summary = self._generate_summary(response)
            print(f"Generated summary: {summary}")
            
            # Get the requested format from the parsed query
            requested_format = parsed.get('format', 'text')
            print(f"Requested format: {requested_format}")
            
            return AnalysisResponse(
                query=query,
                response=response,
                summary=summary,
                data=weather_data,
                format=requested_format  # Use the format from parsed query
            )
            
        except Exception as e:
            print(f"ERROR in analyze_weather: {str(e)}")
            logger.error(f"Error analyzing weather: {str(e)}")
            raise Exception(f"Error analyzing weather: {str(e)}")
            
    def _generate_summary(self, weather: WeatherResponse) -> str:
        """Generate a text summary of the weather data"""
        try:
            if len(weather.forecast) == 1:
                # Current weather
                current = weather.forecast[0]
                return f"Current weather in {weather.city}:\n" \
                       f"Temperature: {current.temperature:.1f}°C\n" \
                       f"Humidity: {current.humidity}%\n" \
                       f"Wind Speed: {current.windSpeed} m/s\n" \
                       f"Conditions: {current.description}\n" \
                       f"Last updated: {weather.generated_at}"
            else:
                # Historical data
                avg_temp = sum(f.temperature for f in weather.forecast) / len(weather.forecast)
                max_temp = max(f.temperature for f in weather.forecast)
                min_temp = min(f.temperature for f in weather.forecast)
                
                return f"Weather data for {weather.city}:\n" \
                       f"Average temperature: {avg_temp:.1f}°C\n" \
                       f"Maximum temperature: {max_temp:.1f}°C\n" \
                       f"Minimum temperature: {min_temp:.1f}°C\n" \
                       f"Data generated at: {weather.generated_at}"
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return f"Weather data for {weather.city} (generated at {weather.generated_at})" 