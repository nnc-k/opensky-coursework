"""
Модуль с моделями данных.

Содержит dataclass-модели для представления стран и воздушных судов.
Использование типизации гарантирует корректность передаваемых данных.
"""

from dataclasses import dataclass


@dataclass
class Country:
    """
    Модель страны для хранения географических координат (bounding box).
    """

    name: str
    iso_code: str | None
    lamin: float  # Минимальная широта (юг)
    lomin: float  # Минимальная долгота (запад)
    lamax: float  # Максимальная широта (север)
    lomax: float  # Максимальная долгота (восток)


@dataclass
class Aeroplane:
    """
    Модель воздушного судна, находящегося в воздушном пространстве.
    """

    icao24: str  # Уникальный идентификатор
    callsign: str | None  # Позывной (может отсутствовать)
    origin_country: str  # Страна регистрации
    longitude: float | None  # Долгота
    latitude: float | None  # Широта
    altitude: float | None  # Высота
    velocity: float | None  # Скорость
    heading: float | None  # Направление
    on_ground: bool  # На земле или в воздухе
    country_id: int | None = None  # Связь с таблицей стран
