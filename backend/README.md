# WeatherAI Backend

This is the backend service for the WeatherAI project, providing AI-powered weather forecasting and analysis capabilities through a RESTful API.

## 🚀 Features

- FastAPI-based REST API
- AI-powered weather forecasting
- Historical weather data analysis
- Integration with weather data sources
- CORS-enabled for frontend integration

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and settings management
- **Pandas & NumPy**: Data manipulation and analysis
- **Transformers & PyTorch**: AI/ML capabilities
- **Meteostat**: Weather data access

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/          # API routes and endpoints
│   ├── core/         # Core application configuration
│   ├── models/       # Data models and schemas
│   ├── services/     # Business logic and services
│   ├── utils/        # Utility functions
│   └── main.py       # Application entry point
├── data/             # Data storage and datasets
├── scripts/          # Utility scripts
├── venv/             # Python virtual environment
└── requirements.txt  # Python dependencies
```

## 🔄 How It Works

### Core Components

1. **Data Collection & Processing**
   - Historical weather data is collected from Meteostat
   - Data is preprocessed and normalized for model training

2. **AI/ML Pipeline**
   - Utilizes transformer-based models for weather prediction
   - Processes historical data to identify patterns and trends
   - Generates forecasts based on learned patterns

3. **API Layer**
   - RESTful endpoints for weather data access
   - Real-time weather forecasting
   - Historical data analysis endpoints

### Workflow

1. **Data Ingestion**
   ```
   External Sources → Data Collection → Preprocessing → Storage
   ```

2. **Model Processing**
   ```
   Historical Data → Feature Engineering → Model Training → Prediction
   ```

3. **API Request Flow**
   ```
   Client Request → API Endpoint → Service Layer → Model Inference → Response
   ```

### Key Features

- **Real-time Forecasting**: Provides up-to-date weather predictions
- **Historical Analysis**: Analyzes past weather patterns and trends
- **Data Integration**: Combines multiple data sources for comprehensive analysis
- **Scalable Architecture**: Built to handle multiple concurrent requests
- **Error Handling**: Robust error management and logging

## 📊 Data Generation and Query Types

### CSV Generation Script
The backend includes a script that generates CSV files containing weather data. This script is used to:
- Collect and process weather data from various sources
- Format the data into structured CSV files
- Store the data for future analysis and forecasting

### Query Types and Data Handling

1. **Current Weather Queries**
   - Uses OpenWeatherMap API exclusively
   - Provides real-time weather data
   - Returns a single weather data point
   - No historical data is fetched for these queries

2. **Forecast Queries**
   - Retrieves exactly 30 days of historical data
   - Uses this historical data to generate accurate forecasts
   - Returns multiple forecast data points
   - Combines historical patterns with current conditions

3. **Historical Queries**
   - Fetches historical data based on specified date range/duration
   - Returns complete historical data points
   - Supports flexible time period selection
   - Provides detailed historical weather analysis

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add necessary configuration variables

### Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file with the following variables:

```
# Add your configuration variables here
```

