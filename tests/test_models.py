"""
Тесты для модуля models.
"""

from src.models import Aeroplane, Country


def test_country_creation() -> None:
    """Проверяет корректное создание модели Country."""
    country = Country(name="TestLand", iso_code="TL", lamin=1.1, lomin=2.2, lamax=3.3, lomax=4.4)
    assert country.name == "TestLand"
    assert country.iso_code == "TL"
    assert country.lamin == 1.1


def test_aeroplane_creation() -> None:
    """Проверяет корректное создание модели Aeroplane."""
    plane = Aeroplane(
        icao24="abc123",
        callsign="TEST",
        origin_country="TestLand",
        longitude=10.0,
        latitude=20.0,
        altitude=1000.0,
        velocity=250.0,
        heading=90.0,
        on_ground=False,
    )
    assert plane.icao24 == "abc123"
    assert plane.callsign == "TEST"
    assert plane.country_id is None
