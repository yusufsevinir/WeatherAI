import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging
from pathlib import Path
from app.core.config import settings
from meteostat import Point, Daily

logger = logging.getLogger(__name__)

class TimeSeriesDataManager:
    def __init__(self):
        self.cache = {}
        self._initialize_cache()
        
    def _initialize_cache(self):
        """Initialize cache with weather stations data"""
        print("\n=== Initializing Data Manager Cache ===")
        self.cache['stations'] = self._load_stations_data()
        print(f"Cache initialized with {len(self.cache['stations'])} stations")
        print("=====================================\n")
        
    def _load_stations_data(self) -> pd.DataFrame:
        """Load weather stations data"""
        try:
            print("\n=== Loading Weather Stations Data ===")
            logger.info("Loading weather stations data")
            
            # Try to load from CSV first
            csv_path = Path("data/weather/capital_cities_weather.csv")
            print(f"Looking for CSV at: {csv_path.absolute()}")
            if csv_path.exists():
                print("Found CSV file, loading data...")
                df = pd.read_csv(csv_path)
                # Get unique cities with their coordinates
                stations_df = df[['city', 'latitude', 'longitude']].drop_duplicates()
                
                # Add country information
                stations_df['country'] = stations_df['city'].apply(self._get_country)
                stations_df['station_id'] = stations_df['city']
                stations_df['city_name'] = stations_df['city']
                
                # Add a searchable name column (lowercase, no special characters)
                stations_df['search_name'] = stations_df['city_name'].str.lower().str.replace(r'[^a-z0-9\s]', '')
                
                print(f"Successfully loaded {len(stations_df)} stations from CSV")
                print(f"Sample stations:\n{stations_df.head(2)}")
                logger.info(f"Loaded {len(stations_df)} weather stations from CSV")
                return stations_df
            
            # Fallback to hardcoded data if CSV doesn't exist
            print("CSV file not found, using hardcoded data")
            logger.warning("CSV file not found, using hardcoded data")
            
            # Define major cities with their coordinates
            stations_data = {
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
            
            # Convert to DataFrame
            df = pd.DataFrame([
                {
                    'station_id': city,
                    'city_name': city,
                    'latitude': lat,
                    'longitude': lon,
                    'country': self._get_country(city)
                }
                for city, (lat, lon) in stations_data.items()
            ])
            
            # Add a searchable name column (lowercase, no special characters)
            df['search_name'] = df['city_name'].str.lower().str.replace(r'[^a-z0-9\s]', '')
            
            logger.info(f"Loaded {len(df)} weather stations from hardcoded data")
            return df
        except Exception as e:
            logger.error(f"Error loading weather stations: {e}")
            return pd.DataFrame()
            
    def _get_country(self, city: str) -> str:
        """Get country for a city"""
        country_map = {
            'London': 'United Kingdom',
            'Paris': 'France',
            'Berlin': 'Germany',
            'Rome': 'Italy',
            'Madrid': 'Spain',
            'Amsterdam': 'Netherlands',
            'Brussels': 'Belgium',
            'Vienna': 'Austria',
            'Bern': 'Switzerland',
            'Oslo': 'Norway',
            'Stockholm': 'Sweden',
            'Copenhagen': 'Denmark',
            'Helsinki': 'Finland',
            'Dublin': 'Ireland',
            'Lisbon': 'Portugal',
            'Athens': 'Greece',
            'Warsaw': 'Poland',
            'Prague': 'Czech Republic',
            'Budapest': 'Hungary',
            'Bucharest': 'Romania',
            'Istanbul': 'Turkey',
            'Moscow': 'Russia',
            'Tokyo': 'Japan',
            'Beijing': 'China',
            'New York': 'United States',
            'Los Angeles': 'United States',
            'Sydney': 'Australia',
            'Dubai': 'United Arab Emirates',
            'Singapore': 'Singapore',
            'Mumbai': 'India'
        }
        return country_map.get(city, 'Unknown')
            
    def get_location_data(self, location: str) -> Optional[Dict[str, Any]]:
        """Get data for a specific location"""
        try:
            print(f"\n=== Getting Location Data ===")
            print(f"Searching for location: {location}")
            logger.info(f"Getting location data for {location}")
            stations_df = self.cache['stations']
            
            if stations_df.empty:
                print("ERROR: No stations data available in cache")
                logger.error("No stations data available")
                return None
            
            # Clean the search location
            search_location = location.lower().strip()
            print(f"Cleaned search location: {search_location}")
            
            # Try exact match first
            location_data = stations_df[stations_df['city_name'].str.lower() == search_location]
            print(f"Exact match results: {len(location_data)} rows")
            
            # If no exact match, try partial match
            if location_data.empty:
                print("No exact match found, trying partial match...")
                location_data = stations_df[stations_df['city_name'].str.lower().str.contains(search_location)]
                if not location_data.empty:
                    print(f"Found partial match: {location_data['city_name'].tolist()}")
                    logger.info(f"Found partial match for {location}: {location_data['city_name'].tolist()}")
            
            # If still no match, try fuzzy matching
            if location_data.empty:
                print("No partial match found, trying fuzzy match...")
                from difflib import get_close_matches
                matches = get_close_matches(search_location, stations_df['city_name'].str.lower().tolist(), n=1, cutoff=0.6)
                if matches:
                    print(f"Found fuzzy match: {matches[0]}")
                    location_data = stations_df[stations_df['city_name'].str.lower() == matches[0]]
                    logger.info(f"Found fuzzy match for {location}: {location_data['city_name'].tolist()}")
            
            if location_data.empty:
                print(f"ERROR: Location {location} not found in stations")
                logger.warning(f"Location {location} not found in stations")
                return None
                
            result = {
                'id': location_data.iloc[0]['station_id'],
                'name': location_data.iloc[0]['city_name'],
                'country': location_data.iloc[0]['country'],
                'latitude': location_data.iloc[0]['latitude'],
                'longitude': location_data.iloc[0]['longitude']
            }
            print(f"Found location data: {result}")
            logger.info(f"Found location data: {result}")
            return result
        except Exception as e:
            print(f"ERROR in get_location_data: {str(e)}")
            logger.error(f"Error getting location data: {e}")
            return None
            
    def get_available_locations(self) -> List[Dict[str, Any]]:
        """Get list of available weather stations"""
        try:
            locations = []
            for _, row in self.cache['stations'].iterrows():
                locations.append({
                    'id': row['station_id'],
                    'name': row['city_name'],
                    'country': row['country'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude']
                })
            return locations
        except Exception as e:
            logger.error(f"Error getting available locations: {e}")
            return []

# Create a singleton instance
data_manager = TimeSeriesDataManager()

# Export function for backward compatibility
def get_location_data(location: str) -> Optional[Dict[str, Any]]:
    """Get location data"""
    return data_manager.get_location_data(location)

def load_historical_data() -> pd.DataFrame:
    """Load all historical weather data"""
    return data_manager.get_historical_weather(
        data_manager.cache['cities'].iloc[0]['city_name'],
        start_date=data_manager.cache['date_range']['min_date'].strftime('%Y-%m-%d'),
        end_date=data_manager.cache['date_range']['max_date'].strftime('%Y-%m-%d')
    )

def load_cities_data() -> pd.DataFrame:
    """Load cities data"""
    return data_manager.cache['cities']

def load_countries_data() -> pd.DataFrame:
    """Load countries data"""
    return data_manager.cache['countries']

def get_historical_weather(location: str, start_date: Optional[str] = None, 
                         end_date: Optional[str] = None) -> pd.DataFrame:
    """Get historical weather data"""
    return data_manager.get_historical_weather(location, start_date, end_date)

def generate_sample_data() -> pd.DataFrame:
    """
    Generate sample historical weather data for testing
    """
    cities = ['London', 'New York', 'Tokyo', 'Sydney', 'Mumbai']
    data = []
    
    # Generate 30 days of historical data for each city
    for city in cities:
        base_temp = np.random.uniform(15, 25)  # Base temperature for each city
        base_humidity = np.random.uniform(60, 80)
        base_wind = np.random.uniform(5, 15)
        
        for i in range(30):
            date = datetime.now() - timedelta(days=30-i)
            
            # Add some daily variation
            temp = base_temp + np.random.normal(0, 3)
            humidity = max(0, min(100, base_humidity + np.random.normal(0, 5)))
            wind = max(0, base_wind + np.random.normal(0, 2))
            
            # Determine weather description
            if temp < 10:
                description = "Cold"
            elif temp < 20:
                description = "Cool"
            elif temp < 25:
                description = "Mild"
            else:
                description = "Warm"
            
            data.append({
                'date': date.isoformat(),
                'temperature': round(temp, 1),
                'humidity': round(humidity, 1),
                'wind_speed': round(wind, 1),
                'description': description,
                'city': city
            })
    
    df = pd.DataFrame(data)
    
    # Save the sample data
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    df.to_csv(os.path.join(settings.DATA_DIR, settings.HISTORICAL_DATA_FILE), index=False)
    
    return df 