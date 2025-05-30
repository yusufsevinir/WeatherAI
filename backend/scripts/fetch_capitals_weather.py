import pandas as pd
from datetime import datetime, timedelta
from meteostat import Point, Daily
import logging
from pathlib import Path
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define capital cities with their coordinates
CAPITAL_CITIES = {
    'London': (51.5074, -0.1278),
    'Paris': (48.8566, 2.3522),
    'Berlin': (52.5200, 13.4050),
    'Rome': (41.9028, 12.4964),
    'Madrid': (40.4168, -3.7038),
    'Amsterdam': (52.3676, 4.9041),
    'Brussels': (50.8503, 4.3517),
    'Vienna': (48.2082, 16.3738),
    'Bern': (46.9480, 7.4474),
    'Oslo': (59.9139, 10.7522),
    'Stockholm': (59.3293, 18.0686),
    'Copenhagen': (55.6761, 12.5683),
    'Helsinki': (60.1699, 24.9384),
    'Dublin': (53.3498, -6.2603),
    'Lisbon': (38.7223, -9.1393),
    'Athens': (37.9838, 23.7275),
    'Warsaw': (52.2297, 21.0122),
    'Prague': (50.0755, 14.4378),
    'Budapest': (47.4979, 19.0402),
    'Bucharest': (44.4268, 26.1025),
    'Istanbul': (41.0082, 28.9784),
    'Moscow': (55.7558, 37.6173),
    'Tokyo': (35.6762, 139.6503),
    'Beijing': (39.9042, 116.4074),
    'New York': (40.7128, -74.0060),
    'Los Angeles': (34.0522, -118.2437),
    'Sydney': (-33.8688, 151.2093),
    'Dubai': (25.2048, 55.2708),
    'Singapore': (1.3521, 103.8198),
    'Mumbai': (19.0760, 72.8777)
}

def fetch_weather_data(city: str, lat: float, lon: float, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Fetch weather data for a specific city using Meteostat."""
    try:
        logger.info(f"Fetching weather data for {city}")
        
        # Create Point object for the city
        location = Point(lat, lon)
        
        # Get daily weather data
        data = Daily(location, start_date, end_date)
        data = data.fetch()
        
        # Add city name
        data['city'] = city
        
        # Reset index to make date a column
        data = data.reset_index()
        
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
        
        return data
        
    except Exception as e:
        logger.error(f"Error fetching data for {city}: {e}")
        return pd.DataFrame()

def main():
    # Create data directory if it doesn't exist
    data_dir = Path("data/weather")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Set date range (last 2 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2*365)
    
    # Fetch data for each capital city
    all_data = []
    for city, (lat, lon) in CAPITAL_CITIES.items():
        df = fetch_weather_data(city, lat, lon, start_date, end_date)
        if not df.empty:
            all_data.append(df)
            logger.info(f"Successfully fetched data for {city}")
    
    if all_data:
        # Combine all data
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # Save to CSV
        output_file = data_dir / "capital_cities_weather.csv"
        combined_data.to_csv(output_file, index=False)
        logger.info(f"Saved weather data to {output_file}")
        
        # Print summary
        print("\nData Summary:")
        print(f"Total cities: {len(all_data)}")
        print(f"Date range: {start_date.date()} to {end_date.date()}")
        print(f"Total records: {len(combined_data)}")
        print("\nColumns available:")
        print(combined_data.columns.tolist())
    else:
        logger.error("No data was fetched for any city")

if __name__ == "__main__":
    main() 