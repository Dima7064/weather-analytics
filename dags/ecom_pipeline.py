from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# 5.4. Настройки по умолчанию (ретраи, владелец, время)
default_args = {
    "owner": "data_team",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,  # Если упадет, попробует 2 раза
    "retry_delay": timedelta(minutes=1),  # Задержка между попытками 1 минута
    "execution_timeout": timedelta(minutes=15),  # Если висит >15 мин - убить
}

# Определяем DAG
with DAG(
    dag_id="ecom_analytics_pipeline",
    default_args=default_args,
    description="Daily ETL pipeline for ecommerce",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",  # Запускать раз в день
    catchup=False,  # Не делать бэкфилл прошлых дат при включении
    tags=["ecom", "daily"],
) as dag:
    # Задача 1: Генерация CSV
    generate_data = BashOperator(
        task_id="generate_data",
        bash_command="cd /opt/airflow && python -m ecom_ingest.cli generate-data",
    )

    # Задача 2: Загрузка в Postgres
    ingest_data = BashOperator(
        task_id="ingest_data",
        bash_command="cd /opt/airflow && python -m ecom_ingest.cli ingest",
    )

    # Задача 3: Запуск dbt
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/airflow/dbt && dbt build --profiles-dir .",
    )

    # Устанавливаем зависимости (Сначала generate, потом ingest, потом dbt)
    generate_data >> ingest_data >> dbt_build
