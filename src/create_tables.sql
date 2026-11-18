-- Удаляем таблицы, если они уже существуют (для удобства перезапуска)
DROP TABLE IF EXISTS aeroplanes;
DROP TABLE IF EXISTS countries;

-- Таблица для хранения стран
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    iso_code VARCHAR(10),
    lamin DOUBLE PRECISION NOT NULL,
    lomin DOUBLE PRECISION NOT NULL,
    lamax DOUBLE PRECISION NOT NULL,
    lomax DOUBLE PRECISION NOT NULL
);

-- Таблица для хранения самолетов
CREATE TABLE aeroplanes (
    id SERIAL PRIMARY KEY,
    icao24 VARCHAR(10) NOT NULL,
    callsign VARCHAR(20),
    origin_country VARCHAR(100),
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    altitude DOUBLE PRECISION,
    velocity DOUBLE PRECISION,
    heading DOUBLE PRECISION,
    on_ground BOOLEAN,
    country_id INTEGER REFERENCES countries(id) ON DELETE CASCADE
);
