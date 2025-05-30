from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class WeatherData(BaseModel):
    date: datetime
    temperature: float
    humidity: float
    windSpeed: float
    pressure: float = 1013.25  # Default sea level pressure in hPa
    description: str
    city: str
    icon: str = "01d"  # Default to clear sky icon

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        alias_generator=lambda s: ''.join([w.capitalize() if i else w for i, w in enumerate(s.split('_'))])
    )

class WeatherResponse(BaseModel):
    forecast: List[WeatherData]
    city: str
    generated_at: datetime

class ForecastRequest(BaseModel):
    query: str
    city: Optional[str] = None
    format: Optional[str] = None  # text, table, or chart
    days: Optional[int] = 7

class AnalysisResponse(BaseModel):
    data: List[WeatherData]
    format: Optional[str] = None  # None, text, table, or chart
    chart_url: Optional[str] = None 