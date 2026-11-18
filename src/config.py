"""
Конфигурационный модуль проекта.
Содержит настройки БД, параметры для API и список стран.
"""

from typing import Final

# --- Настройки базы данных PostgreSQL ---
DB_CONFIG: Final[dict[str, str | int]] = {
    "dbname": "opensky_db",
    "user": "postgres",
    "password": "111297",
    "host": "localhost",
    "port": 5432,
}

# --- Настройки для API ---
USER_AGENT: Final[str] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT: Final[int] = 30

# --- Список стран для отслеживания ---
COUNTRIES_TO_TRACK: Final[list[str]] = [
    "Russia",
    "United States",
    "Germany",
    "France",
    "United Kingdom",
    "China",
    "Japan",
    "Canada",
    "Brazil",
    "Australia",
]

# --- URL для API ---
API_OPENSKY_URL: Final[str] = "https://opensky-network.org/api/states/all"
API_NOMINATIM_URL: Final[str] = "https://nominatim.openstreetmap.org/search"
