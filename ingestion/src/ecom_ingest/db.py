import logging

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

# Наш локальный Postgres из Docker
DB_URL = "postgresql+psycopg://dbt:dbt@localhost:5433/analytics"


def get_engine() -> Engine:
    return create_engine(DB_URL)


def init_db() -> None:
    """Создает схемы и таблицы в Postgres."""
    logger.info("Инициализация базы данных...")
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))

        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS raw.customers (
                customer_id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                country VARCHAR(100),
                signup_date DATE
            );
        """)
        )

        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS raw.products (
                product_id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                category VARCHAR(100),
                price NUMERIC(10, 2)
            );
        """)
        )

        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS raw.orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                status VARCHAR(50),
                order_date TIMESTAMP
            );
        """)
        )
    logger.info("База данных готова.")


def load_csv_to_raw(csv_path: str, table_name: str) -> None:
    """Читает CSV и загружает его в таблицу базы данных."""
    logger.info(f"Загрузка {csv_path} в raw.{table_name}...")
    df = pd.read_csv(csv_path)
    engine = get_engine()

    # Используем pandas to_sql для загрузки
    df.to_sql(
        name=table_name,
        con=engine,
        schema="raw",
        if_exists="replace",  # Перезаписываем таблицу при каждом запуске (для простоты)
        index=False,
        method="multi",
    )
    logger.info(f"Успешно загружено {len(df)} строк в raw.{table_name}.")
