import os
from datetime import datetime

import requests
from dotenv import load_dotenv, find_dotenv
from fastapi import HTTPException


load_dotenv(find_dotenv())

API_KEY = os.getenv("OPEN_WEATHER_KEY")


def get_city_coordinates(city_name: str, country_code: str = None, state_code: str = None):

    base_url = "http://api.openweathermap.org"

    # Construct the URL with optional parameters
    query = f"{city_name}"
    if state_code and country_code == "US":
        query += f",{state_code}"
    if country_code:
        query += f",{country_code}"

    url = f"{base_url}/geo/1.0/direct?q={query}&appid={API_KEY}"

    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error fetching city location."
        )

    return response.json()[0]["lat"], response.json()[0]["lon"]

def get_city_weather_json(lat: float, lon: float, date: datetime):
    
    base_url = "http://api.openweathermap.org"

    url = (
        f"{base_url}/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Error fetching weather information.",
        )
    return response.json()

def parse_weather_json(weather_info: dict, city_name: str, date: datetime):

    main = weather_info.get("main", {})
    temperature = main.get("temp")
    min_temperature = main.get("temp_min")
    max_temperature = main.get("temp_max")
    humidity = main.get("humidity")

    weather_data = {
        "city_name": city_name,
        "date": date,
        "min_temperature": min_temperature,
        "max_temperature": max_temperature,
        "temperature": temperature,
        "humidity": humidity,
    }

    return weather_data

def get_weather(date: str, city_name: str):

    lat, lon = get_city_coordinates(city_name=city_name)
    weather_info = get_city_weather_json(lat=lat, lon=lon, date=date)
    data = parse_weather_json(
        weather_info=weather_info, city_name=city_name, date=date
    )

    return data

if __name__ == '__main__':

    date = "01-01-2000"
    city_name = "NY"

    weather = get_weather(date=date, city_name=city_name)

    print(weather)
