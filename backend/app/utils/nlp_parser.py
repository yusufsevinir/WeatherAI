from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import requests
import os
from dotenv import load_dotenv
import re
import json

# Load environment variables
load_dotenv()

class WeatherQuery(BaseModel):
    """Schema for parsed weather query"""
    location: str = Field(None, description="The city or place the user is asking about")
    duration: int = Field(7, description="Number of days for weather information")
    direction: str = Field("future", description="Whether the query is about past or future weather")
    intent: str = Field("forecast", description="Type of weather information requested (forecast/historical/current)")
    format: str = Field("text", description="Preferred output format (text/table/chart/summary)")

class OpenWeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def validate_city(self, city: str) -> Optional[Dict]:
        """Validate city name and get coordinates"""
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": city,
                "limit": 1,
                "appid": self.api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data:
                return {
                    "name": data[0]["name"],
                    "lat": data[0]["lat"],
                    "lon": data[0]["lon"],
                    "country": data[0]["country"]
                }
            return None
        except Exception as e:
            print(f"Error validating city: {e}")
            return None

    def get_weather(self, city: str, forecast_type: str = "current") -> Optional[Dict]:
        """Get weather data for a city"""
        try:
            # First validate the city
            city_data = self.validate_city(city)
            if not city_data:
                return None

            # Get weather data based on type
            if forecast_type == "current":
                url = f"{self.base_url}/weather"
            elif forecast_type == "forecast":
                url = f"{self.base_url}/forecast"
            else:
                return None

            params = {
                "lat": city_data["lat"],
                "lon": city_data["lon"],
                "appid": self.api_key,
                "units": "metric"  # Use metric units
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Error getting weather data: {e}")
            return None

def get_llm():
    """Initialize and return the text classification pipeline"""
    model_name = "facebook/bart-large-mnli"  # A smaller, efficient model for text understanding
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    pipe = pipeline(
        "zero-shot-classification",
        model=model,
        tokenizer=tokenizer,
        device_map="auto"  # This will automatically use GPU if available
    )
    return pipe

QUERY_TEMPLATE = """
<s>[INST] You are a weather query understanding system. Extract information from the following query and return it in JSON format.

Query: {query}

Extract and return the following information in JSON format:
1. location: The city or place the user is asking about
2. duration: How many days of weather information they want (as a number)
3. direction: Whether they want past or future weather (past/future/current)
4. intent: What type of weather information they want (forecast/historical/current)
5. format: How they want the information presented (text/table/chart/summary)

{format_instructions} [/INST]</s>
"""

def parse_query(query: str) -> Dict[str, Any]:
    """
    Parse natural language query using Google's Gemma 3 27B model through OpenRouter.ai to extract weather request parameters.
    """
    try:
        # Define the prompt for Gemma 3 27B
        prompt = f"""
        Extract the following information from the query: {query}
        Return a JSON object with the following fields:
        - location: The city or place mentioned (e.g., London, Mumbai, Tokyo). If no location is mentioned, use 'London' as default.
        - duration: Number of days (e.g., 3, 7, 30). For current weather queries, use 1.
        - direction: past, future, or current
        - intent: forecast, historical, or current. Use 'current' when the query asks about present weather.
        - format: Choose the most appropriate format based on these rules:
          * Use 'table' when:
            - The query explicitly asks for a table
            - The query asks for multiple days of data (more than 1 day)
            - The query mentions historical data or trends
          * Use 'chart' when:
            - The query explicitly mentions visualization, charts, or graphs
            - The query asks for trends or patterns
          * Use 'text' only when:
            - The query is about current weather
            - The query explicitly asks for a text summary
          * Default to 'table' for multiple days of data

        Examples:
        - "What's the weather like in London?" -> {{"location": "London", "duration": 1, "direction": "current", "intent": "current", "format": "text"}}
        - "Show me the forecast for Tokyo next week" -> {{"location": "Tokyo", "duration": 7, "direction": "future", "intent": "forecast", "format": "table"}}
        - "Show me the weather trends in Paris as a chart" -> {{"location": "Paris", "duration": 30, "direction": "past", "intent": "historical", "format": "chart"}}
        """
        
        # Use the Gemma 3 27B model through OpenRouter.ai
        import requests
        import os
        
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "google/gemma-3-27b-it:free",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        generated_text = response.json()["choices"][0]["message"]["content"]
        
        # Parse the generated text into a structured format
        # Find the JSON object in the generated text
        json_match = re.search(r'\{.*\}', generated_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                parsed = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON from generated text: {json_str}")
                print(f"JSON decode error: {str(e)}")
                # Extract location from query if possible
                location_match = re.search(r'(?:in|for|at)\s+([A-Za-z\s]+)', query)
                location = location_match.group(1).strip() if location_match else "London"
                parsed = {
                    "location": location,
                    "duration": 1,
                    "direction": "current",
                    "intent": "current",
                    "format": "text"
                }
        else:
            print(f"No JSON found in generated text: {generated_text}")
            # Extract location from query if possible
            location_match = re.search(r'(?:in|for|at)\s+([A-Za-z\s]+)', query)
            location = location_match.group(1).strip() if location_match else "London"
            parsed = {
                "location": location,
                "duration": 1,
                "direction": "current",
                "intent": "current",
                "format": "text"
            }
        
        print(f"[parse_query] query: {query} | parsed_format: {parsed.get('format')}")
        print(f"[parse_query] parsed: {parsed}")
        
        # Validate city using OpenWeather API
        weather_api = OpenWeatherAPI()
        if parsed.get("location"):
            city_data = weather_api.validate_city(parsed["location"])
            if city_data:
                parsed["location"] = city_data["name"]  # Use standardized city name
                parsed["coordinates"] = {
                    "lat": city_data["lat"],
                    "lon": city_data["lon"]
                }
                parsed["country"] = city_data["country"]
        
        return parsed
        
    except Exception as e:
        print(f"Error parsing query: {str(e)}")
        # Extract location from query if possible
        location_match = re.search(r'(?:in|for|at)\s+([A-Za-z\s]+)', query)
        location = location_match.group(1).strip() if location_match else "London"
        return {
            "location": location,
            "duration": 1,
            "direction": "current",
            "intent": "current",
            "format": "text"
        }

# Example usage:
if __name__ == "__main__":
    test_queries = [
        "What's the weather going to be like in London next week?",
        "Show me historical weather data for Tokyo last month in a chart",
        "Give me a summary of the current weather in New York",
        "What was the weather like in Paris this weekend?"
    ]
    
    for query in test_queries:
        result = parse_query(query)
        print(f"\nQuery: {query}")
        print(f"Parsed: {json.dumps(result, indent=2)}") 