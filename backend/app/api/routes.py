from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
from app.services.weather_service import WeatherService
from app.models.weather import WeatherResponse, ForecastRequest, AnalysisResponse, WeatherData
import os
import pandas as pd
from pathlib import Path
import random

router = APIRouter()
weather_service = WeatherService()

@router.get("/weather/current", response_model=WeatherResponse)
async def get_current_weather(
    city: str = Query(..., description="City name"),
    country: Optional[str] = Query(None, description="Country name (optional)")
):
    """
    Get current weather for a specific city using OpenWeather API
    """
    try:
        weather = await weather_service.get_current_weather(city, country)
        return weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather/historical", response_model=List[WeatherData])
async def get_historical_weather(
    city: str = Query(..., description="City name"),
    country: Optional[str] = Query(None, description="Country name (optional)"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get historical weather data for a specific city from CSV
    """
    try:
        historical_data = await weather_service.get_historical_data(city, country, start_date, end_date)
        return historical_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/weather/analyze", response_model=AnalysisResponse)
async def analyze_weather(
    request: ForecastRequest
):
    """
    Analyze weather data based on natural language query.
    This endpoint can handle both historical data from CSV and future forecasts.
    The query will be parsed using NLP to determine the type of analysis needed.
    """
    try:
        analysis = await weather_service.analyze_weather(request)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data/convert-parquet-to-csv")
def convert_parquet_to_csv():
    """
    Convert daily_weather.parquet to daily_weather.csv in the data folder.
    """
    try:
        data_dir = Path(__file__).parent.parent.parent / "data"
        parquet_file = data_dir / "daily_weather.parquet"
        csv_file = data_dir / "daily_weather.csv"

        if not parquet_file.exists():
            return JSONResponse(status_code=404, content={"message": f"Parquet file not found at {parquet_file}"})

        df = pd.read_parquet(parquet_file)
        df.to_csv(csv_file, index=False)
        return {"message": f"Conversion successful. CSV saved to {csv_file}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error during conversion: {str(e)}"})

@router.get("/sample-queries", response_model=List[str])
async def get_sample_queries():
    """
    Get dynamically generated sample queries using available city names from the weather data CSV.
    Returns up to 8 diverse queries covering different use cases and formats.
    """
    try:
        data_dir = Path(__file__).parent.parent.parent / "data" / "weather"
        csv_file = data_dir / "capital_cities_weather.csv"
        if not csv_file.exists():
            raise HTTPException(status_code=404, detail=f"Weather data file not found at {csv_file}")
        df = pd.read_csv(csv_file)
        # Get unique city names
        cities = df['city'].dropna().unique().tolist()
        # Select 4 cities if available, otherwise use all available cities
        sample_cities = cities[:6] if len(cities) >= 4 else cities
        print(f"Selected cities for sample queries: {sample_cities}")
        
        # Define query templates by category
        query_templates = {
            "current": [
                "What's the current weather in {city}?",
                "Show me today's weather in {city}",
                "What's the weather like right now in {city}?",
                "Give me the current temperature in {city}"
            ],
            "historical": [
                "Show me the weather in {city} for the past {days} days",
                "What was the weather like in {city} last week?",
                "Show me historical weather data for {city} over the past {days} days",
                "What were the temperature trends in {city} last month?"
            ],
            "forecast": [
                "What's the weather forecast for {city} for the next {days} days?",
                "Show me the {days}-day forecast for {city}",
                "What's the temperature going to be in {city} this week?",
                "Show me the precipitation forecast for {city} over the next {days} days"
            ],
            "format_specific": {
                "table": [
                    "Show me the weather in {city} for the next {days} days in a table format",
                    "Display the temperature trends in {city} as a table",
                    "Show me the weather data for {city} in a tabular format"
                ],
                "chart": [
                    "Show me the temperature trends in {city} as a chart",
                    "Display the precipitation forecast for {city} in a graph",
                    "Show me the weather patterns in {city} as a visualization"
                ],
                "text": [
                    "Give me a text summary of the weather in {city}",
                    "Describe the weather conditions in {city}",
                    "Tell me about the weather in {city}"
                ],
                "summary": [
                    "Summarize the weather in {city} for the past week",
                    "Give me a weather summary for {city}",
                    "Provide a weather overview for {city}"
                ]
            }
        }
        
        # Define time periods and formats
        days = [3, 5, 7]
        formats = ["table", "chart", "text", "summary"]
        
        queries = []
        
        # Generate queries for each city
        for city in sample_cities:
            # Add one query from each category
            queries.append(random.choice(query_templates["current"]).format(city=city))
            
            # Add historical query
            queries.append(random.choice(query_templates["historical"]).format(
                city=city,
                days=random.choice(days)
            ))
            
            # Add forecast query
            queries.append(random.choice(query_templates["forecast"]).format(
                city=city,
                days=random.choice(days)
            ))
            
            # Add format-specific query
            format_type = random.choice(formats)
            queries.append(random.choice(query_templates["format_specific"][format_type]).format(
                city=city,
                days=random.choice(days)
            ))
        
        # Shuffle and limit the number of queries
        random.shuffle(queries)
        return queries[:8]  # Return 8 diverse queries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 