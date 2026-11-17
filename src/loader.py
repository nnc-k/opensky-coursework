"""
Модуль для загрузки данных из API в базу данных PostgreSQL.
"""

import psycopg2
from psycopg2.extras import execute_values

from src.api_client import get_aeroplanes_by_country
from src.config import COUNTRIES_TO_TRACK, DB_CONFIG
from src.country_bounds import COUNTRY_BOUNDS


def load_data() -> None:
    """
    Основная функция загрузки данных: получает координаты стран и самолеты,
    после чего сохраняет их в таблицы countries и aeroplanes.
    """
    print("Начинаем загрузку данных...")

    # Подключаемся к базе данных
    try:
        conn = psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return

    try:
        with conn.cursor() as cur:
            for country_name in COUNTRIES_TO_TRACK:
                print(f"Обработка страны: {country_name}...")

                # 1. Берем координаты из нашего статического словаря (обходим Nominatim)
                country = COUNTRY_BOUNDS.get(country_name)
                if not country:
                    print(f"Нет координат для {country_name}. Пропускаем.")
                    continue

                # 2. Вставляем страну в БД и получаем её ID
                cur.execute(
                    """
                    INSERT INTO countries (name, iso_code, lamin, lomin, lamax, lomax)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO UPDATE 
                    SET lamin = EXCLUDED.lamin, lomin = EXCLUDED.lomin, 
                        lamax = EXCLUDED.lamax, lomax = EXCLUDED.lomax
                    RETURNING id;
                    """,
                    (country.name, country.iso_code, country.lamin, country.lomin, country.lamax, country.lomax),
                )
                country_id = cur.fetchone()[0]

                # 3. Получаем самолеты для этой страны через OpenSky
                aeroplanes = get_aeroplanes_by_country(country)

                if aeroplanes:
                    # 4. Массово вставляем самолеты в БД
                    values = [
                        (
                            a.icao24, a.callsign, a.origin_country, a.longitude,
                            a.latitude, a.altitude, a.velocity, a.heading, a.on_ground, country_id
                        )
                        for a in aeroplanes
                    ]

                    execute_values(
                        cur,
                        """
                        INSERT INTO aeroplanes 
                        (icao24, callsign, origin_country, longitude, latitude, altitude, velocity, heading, on_ground, country_id)
                        VALUES %s
                        """,
                        values,
                    )
                    print(f"  Успешно добавлено {len(aeroplanes)} самолетов.")
                else:
                    print(f"  В воздушном пространстве {country_name} сейчас нет самолетов.")

            # Фиксируем изменения в БД
            conn.commit()
            print("\nЗагрузка данных успешно завершена!")

    except psycopg2.Error as e:
        print(f"Ошибка при работе с БД: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    load_data()
