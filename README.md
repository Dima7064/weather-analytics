# weather-analytics

Платформа аналитики погоды: ingestion → dbt → Airflow → BI.

## Стек

- **Ingestion**: Python (requests, pydantic, typer)
- **Raw**: PostgreSQL
- **DWH**: ClickHouse
- **Трансформация**: dbt-core
- **Оркестрация**: Airflow (Cosmos)
- **BI**: Metabase, Superset
- **Качество**: dbt tests, Elementary
- **Semantic layer**: dbt MetricFlow
- **CI**: GitHub Actions

## Источники данных

- [Open-Meteo](https://open-meteo.com/) — Geocoding, Forecast, Historical, Air Quality (бесплатно, без ключа).

## Структура

weather-analytics/
├── ingestion/ # Python: API-клиент, CLI
├── dbt/ # dbt-проект
├── airflow/ # DAG'и
├── bi/ # Metabase/Superset
├── docs/ # ADR, runbooks
├── tests/ # общие тесты
└── .github/ # CI

## Быстрый старт

1. `docker compose up -d` — Postgres, ClickHouse, Metabase.
2. `uv sync --all-extras` — зависимости.
3. `uv run pytest` — тесты.
4. CLI и dbt появятся на следующих этапах.

## Разработка

- `uv run ruff check .` — линтер.
- `uv run ruff format .` — форматтер.
- `uv run mypy ingestion/src tests` — типы.
- `uv run pytest` — тесты.
- `uv run pre-commit run --all-files` — хуки.

## Лицензия

MIT
