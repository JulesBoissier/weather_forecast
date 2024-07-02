import unittest
from unittest.mock import patch, Mock

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

class TestApp(unittest.TestCase):

    response_dict = {
        "city_name": "Paris",
        "date": "01-01-2015",
        "min_temperature": 292.57,
        "max_temperature": 294.47,
        "temperature": 293.81,
        "humidity": 65,
    }

    #Need to patch weather service
    @patch("app.weather_service.WeatherService.get_weather")
    def test_positive_response(self, mock_get_weather):

        mock_get_weather.return_value = self.response_dict

        with TestClient(app) as client:
            response = client.get("/city_weather?city_name=Paris&date=01-01-2015")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.response_dict)
