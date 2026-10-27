# Runbook: Сбой пайплайна ecom_analytics_pipeline

## Симптомы

В Airflow DAG `ecom_analytics_pipeline` упал со статусом `Failed` на этапе `dbt_build`.

## Что делать (Step-by-step)

1. Зайти в Airflow -> DAG -> Кликнуть на красный квадратик `dbt_build` -> Открыть **Logs**.
2. Найти в логах строчку со словом `ERROR` или `FAIL`.
3. Если ошибка связана с тестом (`test`):
   - Зайти в базу данных и посмотреть, какие строки нарушили правило (например, `SELECT * FROM raw.orders WHERE quantity <= 0`).
   - Связаться с командой, которая генерирует данные (в нашем случае это Python-скрипт).
4. Если ошибка связана с базой данных (`connection refused`):
   - Проверить, запущен ли контейнер Postgres (`docker compose ps`).
5. После исправления данных зайти в Airflow и нажать **Clear task** (Очистить) для упавшей задачи.
