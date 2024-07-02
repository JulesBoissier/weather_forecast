from sqlalchemy.orm import Session
from app.database.database import Weather, get_weather, create_weather
from app.clients.open_weather_client import OpenWeatherClient

class WeatherService:
    def __init__(self, db: Session, api_client: OpenWeatherClient):
        self.db = db
        self.api_client = api_client

    def get_weather(self, city_name: str, date: str):
        weather = get_weather(self.db, city_name, date)
        if weather:
            return weather

        weather_data = self.api_client.get_weather(date = date, city_name = city_name)

        weather_record = Weather(
            city=city_name,
            date=date,
            min_temp=weather_data["min_temperature"],
            max_temp=weather_data["max_temperature"],
            avg_temp=weather_data["temperature"],
            humidity=weather_data["humidity"],
        )
        create_weather(self.db, weather_record)
        return weather_record
