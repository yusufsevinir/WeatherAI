from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "WeatherAI"
    
    # Weather API Settings
    OPENWEATHER_API_KEY: Optional[str] = None
    
    # OpenRouter API Settings
    OPENROUTER_API_KEY: Optional[str] = None
    
    # Model Settings
    FORECAST_DAYS: int = 7
    DEFAULT_CITY: str = "London"
    
    # Data Settings
    DATA_DIR: str = "data"
    HISTORICAL_DATA_FILE: str = "capital_cities_weather.csv"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 