import unittest
from unittest.mock import patch, MagicMock

from fastapi import HTTPException
from requests.exceptions import HTTPError


from app.clients.open_weather_client import OpenWeatherClient

class TestOpenWeatherClient(unittest.TestCase):

    @staticmethod
    def _mock_response_setup(mock_response):
        mock = MagicMock()
        mock.json.return_value = mock_response
        mock.status_code = 200
        return mock

    def test_initialization(self):
        api_key = "12345"

        client = OpenWeatherClient(api_key = api_key)

        self.assertEqual(client.api_key, api_key)
        self.assertEqual(client.base_url, "http://api.openweathermap.org")

    @patch("app.clients.open_weather_client.requests.get")
    def test_get_city_coordinates(self, mock_get):
        city_latitude = 100
        city_longitude = 42

        mock_response = self._mock_response_setup(
            [{"lat": city_latitude, "lon": city_longitude}]
        )
        mock_get.return_value = mock_response

        client = OpenWeatherClient(api_key="123")
        lat, lon = client._get_city_coordinates("London")

        self.assertEqual(lat, city_latitude)
        self.assertEqual(lon, city_longitude)

    def test_get_city_weather_json(self):
        pass

    def test_parse_weather_json(self):
        pass

    @patch.object(OpenWeatherClient, "_get_city_coordinates")
    @patch.object(OpenWeatherClient, "_get_city_weather_json")
    @patch.object(OpenWeatherClient, "_parse_weather_json")
    def test_get_weather(
        self, mock_parse_weather, mock_get_weather_json, mock_get_coordinates
    ):
        # Mock data
        mock_weather_info = {
            "main": {
                "temp": 293.15,
                "temp_min": 292.57,
                "temp_max": 294.82,
                "humidity": 70,
            }
        }
        mock_parsed_data = {
            "city_name": "Paris",
            "date": "2024-07-02",
            "min_temperature": 292.57,
            "max_temperature": 294.82,
            "temperature": 293.15,
            "humidity": 70,
        }

        date = "2024-07-02"
        city_name = "Paris"

        # Configure mocks
        mock_get_coordinates.return_value = (42, 24)
        mock_get_weather_json.return_value = mock_weather_info
        mock_parse_weather.return_value = mock_parsed_data

        # Create client instance
        client = OpenWeatherClient(api_key="test_api_key")
        weather_data = client.get_weather(date=date, city_name=city_name)

        # Validate returned values
        mock_get_coordinates.assert_called_once_with(city_name=city_name)
        mock_get_weather_json.assert_called_once_with(
            lat=42, lon=24, date=date
        )
        mock_parse_weather.assert_called_once_with(
            weather_info=mock_weather_info, city_name=city_name, date=date
        )
        self.assertEqual(weather_data, mock_parsed_data)

    @patch.object(
        OpenWeatherClient,
        "_get_city_coordinates",
        side_effect=HTTPError("City not found"),
    )
    def test_get_weather_error_handling(self, mock_get_coordinates):
        # Create instance of OpenWeatherClient (mocking the API key for test)
        client = OpenWeatherClient(api_key="test_api_key")

        # Call the method under test with invalid city name to trigger exception
        with self.assertRaises(HTTPError):
            client.get_weather(date="2024-07-02", city_name="FakeCity")
