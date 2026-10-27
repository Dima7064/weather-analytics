from datetime import datetime, timedelta
import logging
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

logger = logging.getLogger(__name__)

# Функция-алерт, которая будет вызываться при ошибке
def alert_on_failure(context):
    task_instance = context.get("task_instance")
    dag_id = context.get("dag").dag_id
    error_msg = f"КРИТИЧЕСКАЯ ОШИБКА в DAG {dag_id}! Задача {task_instance.task_id} упала."

    # В реальности здесь был бы requests.post(SLACK_WEBHOOK_URL, json={"text": error_msg})
    logger.error(error_msg)
    print(f"=== ОТПРАВКА АЛЕРТА В SLACK ===\n{error_msg}\n================================")

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': alert_on_failure, # <-- Подключаем алерт
}

with DAG(
    dag_id='ecom_analytics_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline for ecommerce',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['ecom', 'daily'],
) as dag:

    generate_data = BashOperator(
        task_id='generate_data',
        bash_command='cd /opt/airflow && python -m ecom_ingest.cli generate-data',
    )

    ingest_data = BashOperator(
        task_id='ingest_data',
        bash_command='cd /opt/airflow && python -m ecom_ingest.cli ingest',
    )

    # Добавляем шаг с dbt artifacts, чтобы сохранять логи
    dbt_build = BashOperator(
        task_id='dbt_build',
        bash_command='cd /opt/airflow/dbt && dbt deps && dbt build --profiles-dir . && dbt run --select dbt_artifacts --profiles-dir .',
    )

    generate_data >> ingest_data >> dbt_build
