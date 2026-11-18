"""
Модуль с жестко заданными координатами (bounding box) для стран.

Используется для обхода ограничений Nominatim при разработке.
"""

from src.models import Country

# Приблизительные координаты (юг, запад, север, восток) для 10 стран
COUNTRY_BOUNDS: dict[str, Country] = {
    "Russia": Country(name="Russia", iso_code="RU", lamin=41.0, lomin=19.0, lamax=82.0, lomax=180.0),
    "United States": Country(name="United States", iso_code="US", lamin=24.0, lomin=-125.0, lamax=49.0, lomax=-66.0),
    "Germany": Country(name="Germany", iso_code="DE", lamin=47.0, lomin=5.0, lamax=55.0, lomax=15.0),
    "France": Country(name="France", iso_code="FR", lamin=41.0, lomin=-5.0, lamax=51.0, lomax=10.0),
    "United Kingdom": Country(name="United Kingdom", iso_code="GB", lamin=49.0, lomin=-8.0, lamax=61.0, lomax=2.0),
    "China": Country(name="China", iso_code="CN", lamin=18.0, lomin=73.0, lamax=54.0, lomax=135.0),
    "Japan": Country(name="Japan", iso_code="JP", lamin=24.0, lomin=122.0, lamax=46.0, lomax=146.0),
    "Canada": Country(name="Canada", iso_code="CA", lamin=42.0, lomin=-141.0, lamax=83.0, lomax=-52.0),
    "Brazil": Country(name="Brazil", iso_code="BR", lamin=-34.0, lomin=-74.0, lamax=5.0, lomax=-34.0),
    "Australia": Country(name="Australia", iso_code="AU", lamin=-44.0, lomin=112.0, lamax=-10.0, lomax=154.0),
}
