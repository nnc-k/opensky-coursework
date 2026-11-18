"""
Тесты для модуля api_client.
Используют mock, чтобы не делать реальные запросы в интернет.
"""

from unittest.mock import MagicMock, patch

from src.api_client import get_aeroplanes_by_country, get_country_coordinates
from src.models import Country


@patch("src.api_client.requests.get")
def test_get_country_coordinates_success(mock_get: MagicMock) -> None:
    """Проверяет успешное получение координат страны."""
    mock_response = MagicMock()
    mock_response.json.return_value = [{"boundingbox": ["10.0", "20.0", "30.0", "40.0"]}]
    mock_get.return_value = mock_response

    country = get_country_coordinates("TestCountry")

    assert country is not None
    assert country.name == "TestCountry"
    assert country.lamin == 10.0
    assert country.lomax == 40.0


@patch("src.api_client.requests.get")
def test_get_aeroplanes_by_country_success(mock_get: MagicMock) -> None:
    """Проверяет успешное получение списка самолетов для страны."""
    mock_response = MagicMock()
    # Имитируем ответ OpenSky: массив состояний
    mock_response.json.return_value = {
        "states": [["abc123", "TESTFLIGHT ", "TestLand", 12345, 12345, 10.0, 20.0, 1000.0, False, 250.0, 90.0]]
    }
    mock_get.return_value = mock_response

    country = Country(name="TestLand", iso_code="TL", lamin=0, lomin=0, lamax=1, lomax=1)
    aeroplanes = get_aeroplanes_by_country(country)

    assert len(aeroplanes) == 1
    assert aeroplanes[0].icao24 == "abc123"
    assert aeroplanes[0].callsign == "TESTFLIGHT"  # Проверяем, что .strip() сработал
    assert aeroplanes[0].velocity == 250.0
