# Weather Forecast

A quick weather forecasting project allowing users to query the weather for any given city.

Disclaimer: From my findings, there is no free access with open_weather to historical and future weather forecast, so this project only covers present weather. It still takes in a mock 'date' argument, and the feature could be fairly easily implemented if required.

## How to Run

### Pre-requisites

- Python 3.9
- pip
- Docker (Optional)

### Setup

1. Clone the repository:

- git clone https://github.com/your_username/project_name.git
- cd project_name

2. Install dependencies:

- pip install -r requirements.txt

3. Set OpenWeather API Key as Environment Variables:

- Get the API key here: https://openweathermap.org/api

- Set it with: export OPEN_WEATHER_KEY="api-key"

- Or store it in a .env file with OPEN_WEATHER_KEY="api-key"

4. Run the Application locally:

- fastapi run app/main.py --host 0.0.0.0 --port 80

### Optional - using Docker

1. Build the Docker Image

- docker-compose build

2. Run the Docker container

- docker-compose up

## Using the App

You can then query the API end-point following this structure:

http://localhost:8000/city_weather?city_name=Paris&date=01-01-2015

You're free to change the city_name and date to any real values

## TODOs:

-Add more unit-tests coverage (SQLite, WeatherService, OpenWeatherClient)
-Add support for State and Country code to App API End-point
