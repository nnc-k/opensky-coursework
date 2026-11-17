"""
Тесты для класса DBManager с использованием mock (без реального подключения к БД).
"""

from unittest.mock import MagicMock, patch

import pytest

from src.db_manager import DBManager


@pytest.fixture
def mock_db() -> DBManager:
    """Фикстура для создания DBManager с поддельным подключением к БД."""
    with patch("src.db_manager.psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        db = DBManager({"dbname": "test"})
        return db


@patch("src.db_manager.psycopg2.connect")
def test_get_countries_and_aeroplanes_count(mock_connect: MagicMock) -> None:
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("Russia", 10), ("USA", 20)]
    mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DBManager({"dbname": "test"})
    result = db.get_countries_and_aeroplanes_count()

    assert result == [("Russia", 10), ("USA", 20)]
    mock_cursor.execute.assert_called_once()


@patch("src.db_manager.psycopg2.connect")
def test_get_avg_speed(mock_connect: MagicMock) -> None:
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (250.5,)
    mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DBManager({"dbname": "test"})
    result = db.get_avg_speed()

    assert result == 250.5


@patch("src.db_manager.psycopg2.connect")
def test_get_aeroplanes_with_keyword(mock_connect: MagicMock) -> None:
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("abc", "ACA123")]
    mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DBManager({"dbname": "test"})
    result = db.get_aeroplanes_with_keyword("ACA")

    assert result == [("abc", "ACA123")]
    # Проверяем, что запрос вызван с правильным параметром (ILIKE %ACA%)
    mock_cursor.execute.assert_called_once()
    args, kwargs = mock_cursor.execute.call_args
    assert "%ACA%" in args[1]
