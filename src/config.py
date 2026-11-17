"""
Конфигурационный модуль проекта.

Содержит настройки подключения к базе данных PostgreSQL,
параметры для запросов к API и список отслеживаемых стран.
"""

from typing import Final

# --- Настройки базы данных PostgreSQL ---
DB_CONFIG: Final[dict[str, str | int]] = {
    "dbname": "opensky_db",
    "user": "postgres",
    "password": "111297"
    "host": "localhost",
    "port": 5432,
}

# --- Настройки для API ---
USER_AGENT: Final[str] = "Coursework_OpenSky_Project/1.0 (student@example.com)"
REQUEST_TIMEOUT: Final[int] = 30

# --- Список стран для отслеживания (минимум 10 для критерия) ---
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
API_NOMINATIM_URL: str = "https://nominatim.openstreetmap.org/search"