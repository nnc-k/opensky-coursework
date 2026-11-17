"""
Модуль для работы с внешними API.

Содержит функции для получения географических координат стран
через Nominatim и данных о самолетах через OpenSky Network.
"""

import time
from typing import Any

import requests

from src.config import API_NOMINATIM_URL, API_OPENSKY_URL, REQUEST_TIMEOUT, USER_AGENT
from src.models import Aeroplane, Country


def get_country_coordinates(country_name: str) -> Country | None:
    """
    Получает координаты (bounding box) страны через Nominatim API.

    :param country_name: Название страны на английском языке.
    :return: Объект Country с координатами или None, если страна не найдена.
    """
    params = {
        "q": country_name,
        "format": "json",
        "limit": 1,
    }
    headers = {"User-Agent": USER_AGENT}

    try:
        response = requests.get(API_NOMINATIM_URL, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if not data:
            print(f"Страна не найдена: {country_name}")
            return None

        # boundingbox в Nominatim возвращается в порядке: [юг, север, запад, восток]
        bbox = list(map(float, data[0]["boundingbox"]))

        # Соблюдаем правила Nominatim: не более 1 запроса в секунду
        time.sleep(1.1)

        return Country(
            name=country_name,
            iso_code=None,
            lamin=bbox[0],
            lamax=bbox[1],
            lomin=bbox[2],
            lomax=bbox[3],
        )

    except requests.RequestException as e:
        print(f"Ошибка при запросе к Nominatim для {country_name}: {e}")
        return None


def get_aeroplanes_by_country(country: Country) -> list[Aeroplane]:
    """
    Получает список самолетов в воздушном пространстве страны через OpenSky API.

    :param country: Объект Country с координатами для поиска.
    :return: Список объектов Aeroplane.
    """
    params = {
        "lamin": country.lamin,
        "lomin": country.lomin,
        "lamax": country.lamax,
        "lomax": country.lomax,
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    aeroplanes = []

    try:
        response = requests.get(API_OPENSKY_URL, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data: dict[str, Any] = response.json()

        states = data.get("states")
        if not states:
            return []

        for state in states:
            # state - это массив с фиксированными индексами по документации OpenSky
            aeroplane = Aeroplane(
                icao24=state[0],
                callsign=state[1].strip() if state[1] else None,
                origin_country=state[2],
                longitude=state[5],
                latitude=state[6],
                altitude=state[7],
                on_ground=state[8],
                velocity=state[9],
                heading=state[10],
                country_id=None,
            )
            aeroplanes.append(aeroplane)

        return aeroplanes

    except requests.RequestException as e:
        print(f"Ошибка при запросе к OpenSky для {country.name}: {e}")
        return []
