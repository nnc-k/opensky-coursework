"""
Главный модуль приложения.

Связывает настройки, базу данных и класс DBManager для вывода статистики.
"""

from src.config import DB_CONFIG
from src.db_manager import DBManager


def main() -> None:
    """
    Точка входа в программу. Демонстрирует работу всех методов DBManager.
    """
    print("Подключение к базе данных...")

    try:
        db = DBManager(DB_CONFIG)
    except Exception as e:
        print(f"Не удалось подключиться к БД: {e}")
        return

    print("\n" + "=" * 50)
    print("1. СТРАНЫ И КОЛИЧЕСТВО САМОЛЕТОВ")
    print("=" * 50)
    countries_stats = db.get_countries_and_aeroplanes_count()
    for country_name, count in countries_stats:
        print(f"{country_name}: {count} самолетов")

    print("\n" + "=" * 50)
    print("2. ВСЕ ВОЗДУШНЫЕ СУДА (первые 5 для примера)")
    print("=" * 50)
    all_aeroplanes = db.get_all_aeroplanes()
    print(f"Всего в базе: {len(all_aeroplanes)} самолетов.")
    for plane in all_aeroplanes[:5]:
        print(f"Позывной: {plane['callsign']} | Страна: {plane['origin_country']} | Скорость: {plane['velocity']} м/с")

    print("\n" + "=" * 50)
    print("3. СРЕДНЯЯ СКОРОСТЬ")
    print("=" * 50)
    avg_speed = db.get_avg_speed()
    if avg_speed:
        print(f"Средняя скорость всех самолетов: {avg_speed:.2f} м/с")
    else:
        print("Нет данных о скоростях.")

    print("\n" + "=" * 50)
    print("4. САМОЛЕТЫ СО СКОРОСТЬЮ ВЫШЕ СРЕДНЕЙ (первые 5)")
    print("=" * 50)
    faster_planes = db.get_aeroplanes_with_higher_speed()
    print(f"Всего самолетов быстрее средней скорости: {len(faster_planes)}")
    for icao24, callsign, velocity in faster_planes[:5]:
        print(f"ICAO24: {icao24} | Позывной: {callsign} | Скорость: {velocity} м/с")

    print("\n" + "=" * 50)
    print("5. ПОИСК ПО ПОЗЫВНОМУ (ключевое слово 'ACA')")
    print("=" * 50)
    keyword_planes = db.get_aeroplanes_with_keyword("ACA")
    if keyword_planes:
        print(f"Найдено самолетов с 'ACA' в позывном: {len(keyword_planes)}")
        for icao24, callsign in keyword_planes:
            print(f"ICAO24: {icao24} | Позывной: {callsign}")
    else:
        print("Самолетов с таким позывным не найдено (возможно, они сейчас не в воздухе).")


if __name__ == "__main__":
    main()
