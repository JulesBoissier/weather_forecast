import os

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
import uvicorn

from app.clients.open_weather_client import OpenWeatherClient

load_dotenv(find_dotenv())

API_KEY = os.getenv("OPEN_WEATHER_KEY")

app = FastAPI()


@app.get("/city_weather")
def get_city_data(city_name: str, date: str):
    client = OpenWeatherClient(api_key=API_KEY)
    data = client.get_weather(date = date, city_name=city_name)
    return data


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
    # http://127.0.0.1:8000/city_weather?city_name=Paris&date=01-01-2015
