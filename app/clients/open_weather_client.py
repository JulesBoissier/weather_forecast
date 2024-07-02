import os
from datetime import datetime

import requests
from fastapi import HTTPException


class OpenWeatherClient:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org"

    def _get_city_coordinates(
        self, city_name: str, country_code: str = None, state_code: str = None
    ):

        # Construct the URL with optional parameters
        query = f"{city_name}"
        if state_code and country_code == "US": # State code only applicable in the US
            query += f",{state_code}"
        if country_code:
            query += f",{country_code}"

        url = f"{self.base_url}/geo/1.0/direct?q={query}&appid={self.api_key}"

        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error fetching city location."
            )

        return response.json()[0]["lat"], response.json()[0]["lon"]

    def _get_city_weather_json(self, lat: float, lon: float, date: datetime):

        url = (
            f"{self.base_url}/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}"
        )

        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error fetching weather information.",
            )
        return response.json()

    def _parse_weather_json(self, weather_info: dict, city_name: str, date: datetime):

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

    def get_weather(self, date: str, city_name: str):

        lat, lon = self._get_city_coordinates(city_name=city_name)
        weather_info = self._get_city_weather_json(lat=lat, lon=lon, date=date)
        data = self._parse_weather_json(
            weather_info=weather_info, city_name=city_name, date=date
        )

        return data
