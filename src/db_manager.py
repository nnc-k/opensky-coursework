"""
Модуль для работы с базой данных PostgreSQL.

Содержит класс DBManager, который реализует методы для получения
статистики по странам и самолетам.
"""

from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor


class DBManager:
    """
    Класс для управления подключением к БД и выполнения запросов.
    """

    def __init__(self, db_config: dict[str, Any]) -> None:
        """
        Инициализирует подключение к базе данных.

        :param db_config: Словарь с параметрами подключения (dbname, user, password, host, port).
        """
        self.__conn = psycopg2.connect(**db_config)
        self.__conn.autocommit = True

    def __del__(self) -> None:
        """
        Закрывает соединение с БД при удалении объекта.
        """
        if hasattr(self, "_DBManager__conn") and self.__conn:
            self.__conn.close()

    def get_countries_and_aeroplanes_count(self) -> list[tuple[Any, ...]]:
        """
        Получает список всех стран и количество самолетов в их воздушных пространствах.

        :return: Список кортежей (название страны, количество самолетов).
        """
        query = """
            SELECT c.name, COUNT(a.id) AS aeroplanes_count
            FROM countries c
            LEFT JOIN aeroplanes a ON a.country_id = c.id
            GROUP BY c.id, c.name
            ORDER BY c.name;
        """
        with self.__conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def get_all_aeroplanes(self) -> list[dict[str, Any]]:
        """
        Получает список всех воздушных судов.

        :return: Список словарей с полной информацией о самолетах.
        """
        query = "SELECT * FROM aeroplanes ORDER BY id;"
        with self.__conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

    def get_avg_speed(self) -> float | None:
        """
        Получает среднюю скорость по всем самолетам.

        :return: Средняя скорость (float) или None, если данных нет.
        """
        query = "SELECT AVG(velocity) FROM aeroplanes WHERE velocity IS NOT NULL;"
        with self.__conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()
            return result[0] if result else None

    def get_aeroplanes_with_higher_speed(self) -> list[tuple[Any, ...]]:
        """
        Получает список самолетов, скорость которых выше средней.

        :return: Список кортежей (icao24, callsign, velocity).
        """
        query = """
            SELECT icao24, callsign, velocity
            FROM aeroplanes
            WHERE velocity > (SELECT AVG(velocity) FROM aeroplanes)
            ORDER BY velocity DESC;
        """
        with self.__conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def get_aeroplanes_with_keyword(self, keyword: str) -> list[tuple[Any, ...]]:
        """
        Получает список самолетов, в позывном которых содержатся переданные символы.

        :param keyword: Подстрока для поиска (например, 'ACA').
        :return: Список кортежей (icao24, callsign).
        """
        query = """
            SELECT icao24, callsign
            FROM aeroplanes
            WHERE callsign ILIKE %s
            ORDER BY callsign;
        """
        with self.__conn.cursor() as cur:
            # Используем ILIKE для нечувствительного к регистру поиска
            cur.execute(query, (f"%{keyword}%",))
            return cur.fetchall()
