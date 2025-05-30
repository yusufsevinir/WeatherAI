import os
import requests
import logging
from typing import Dict, Optional
from app.utils.data_loader import get_location_data

logger = logging.getLogger(__name__)

class OpenWeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        print(f"\n=== OpenWeatherAPI Initialization ===")
        print(f"API Key present: {'Yes' if self.api_key else 'No'}")
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable is not set")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        print(f"Base URL: {self.base_url}")
        print("=====================================\n")
        
    def get_weather(self, city: str, type: str = "current") -> Optional[Dict]:
        """Get weather data for a city"""
        try:
            print(f"\n=== Getting Weather Data ===")
            print(f"City: {city}")
            print(f"Type: {type}")
            
            # Get location data
            print("Fetching location data...")
            location_data = get_location_data(city)
            if not location_data:
                print(f"Location data not found for {city}")
                logger.error(f"Location data not found for {city}")
                return None
            
            print(f"Location data found: {location_data}")
                
            # Construct API URL
            url = f"{self.base_url}/weather"
            params = {
                "lat": location_data["latitude"],
                "lon": location_data["longitude"],
                "appid": self.api_key,
                "units": "metric"  # Use metric units (Celsius)
            }
            
            print(f"Making API request to: {url}")
            print(f"With parameters: {params}")
            
            # Make API request
            response = requests.get(url, params=params)
            print(f"Response status code: {response.status_code}")
            
            response.raise_for_status()
            data = response.json()
            print(f"Response data: {data}")
            print("==============================\n")
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            logger.error(f"Error getting weather data: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            logger.error(f"Unexpected error: {e}")
            return None 