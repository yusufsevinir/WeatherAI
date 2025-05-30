import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any

def _validate_float(value: float, min_val: float, max_val: float) -> float:
    """Validate and clamp float values to ensure they are within valid ranges"""
    if pd.isna(value) or np.isinf(value):
        return (min_val + max_val) / 2  # Return middle value if invalid
    return max(min_val, min(max_val, value))

def _get_weather_description(temp: float) -> str:
    """Get weather description based on temperature"""
    if temp < 5:
        return "Cold"
    elif temp < 15:
        return "Cool"
    elif temp < 25:
        return "Mild"
    else:
        return "Warm"

def generate_forecast(historical_data: pd.DataFrame, days: int) -> pd.DataFrame:
    """
    Generate weather forecast using historical data
    """
    # Simple moving average forecast
    forecast_data = []
    
    # Convert date strings to datetime objects
    historical_data['date'] = pd.to_datetime(historical_data['date'])
    last_date = historical_data['date'].max()
    
    # Calculate trends and patterns from historical data
    temp_trend = historical_data['temperature'].diff().mean()  # Temperature trend
    temp_std = historical_data['temperature'].std()  # Temperature variation
    temp_mean = historical_data['temperature'].mean()  # Average temperature
    
    humidity_mean = historical_data['humidity'].mean() if 'humidity' in historical_data.columns else 60.0
    humidity_std = historical_data['humidity'].std() if 'humidity' in historical_data.columns else 10.0
    
    wind_mean = historical_data['wind_speed'].mean() if 'wind_speed' in historical_data.columns else 10.0
    wind_std = historical_data['wind_speed'].std() if 'wind_speed' in historical_data.columns else 5.0
    
    pressure_mean = historical_data['pressure'].mean() if 'pressure' in historical_data.columns else 1013.25
    pressure_std = historical_data['pressure'].std() if 'pressure' in historical_data.columns else 5.0
    
    # Generate forecast for each day
    for i in range(days):
        forecast_date = last_date + timedelta(days=i+1)
        
        # Generate temperature with trend and seasonal variation
        temp = temp_mean + (temp_trend * (i + 1)) + np.random.normal(0, temp_std * 0.5)
        temp = _validate_float(temp, -20, 40)  # Reasonable temperature range
        
        # Generate other parameters with realistic variations
        humidity = _validate_float(
            humidity_mean + np.random.normal(0, humidity_std * 0.5),
            20, 100  # Humidity must be between 20% and 100%
        )
        
        wind = _validate_float(
            wind_mean + np.random.normal(0, wind_std * 0.5),
            0, 50  # Reasonable wind speed range
        )
        
        pressure = _validate_float(
            pressure_mean + np.random.normal(0, pressure_std * 0.5),
            950, 1050  # Reasonable pressure range
        )
        
        # Get weather description based on temperature
        description = _get_weather_description(temp)
        
        forecast_data.append({
            'date': forecast_date.isoformat(),
            'temperature': round(temp, 1),
            'humidity': round(humidity, 1),
            'wind_speed': round(wind, 1),
            'pressure': round(pressure, 1),
            'description': description
        })
    
    return pd.DataFrame(forecast_data) 