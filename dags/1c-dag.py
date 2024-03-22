import time
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.docker.operators.docker_swarm import DockerSwarmOperator
from notifiers.tg_notifier import TelegramNotification
from sensors.rmq_sensor import RMQSensor
from airflow import DAG


default_args = {
    "on_failure_callback": TelegramNotification(
        telegram_bot_token=Variable.get("tg_bot_token"),
        telegram_chat_id=Variable.get("alerting_chat_id"),
    )
}

with DAG(
    dag_id="1c",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["rmq", "dbt", "1c"],
    schedule_interval=timedelta(hours=1),
    default_args=default_args,
    description="extract files from 1c RabbitMQ queue to postgres DWH"
) as dag:
    
    rmq_sensor = RMQSensor(
        task_id="rmq_task_1",
        rmq_conn_id="1c_rmq_dev",
        mode="reschedule",
        poke_interval=60 * 3,
        timeout=60 * 59,
        soft_fail=True,
        wait_for_downstream=True,
    )

    import_1c = DockerSwarmOperator(
        task_id="rmq_to_postgres",
        image="af_1c_task:1",
        api_version="auto",
        docker_url="unix://var/run/docker.sock",
        networks=["bridge", "superset_superset"],
        auto_remove=True,
        environment={
            "MAX_BATCH_SIZE": Variable.get("MAX_BATCH_SIZE"),
            "QUEUE": Variable.get("QUEUE"),
            "MQ_HOST": Variable.get("MQ_HOST"),
            "MQ_PORT": Variable.get("MQ_PORT"),
            "MQ_VHOST": Variable.get("MQ_VHOST"),
            "MQ_LOGIN": Variable.get("MQ_LOGIN"),
            "MQ_PASS": Variable.get("MQ_PASS"),
            "HEARTBEAT": Variable.get("HEARTBEAT"),
            "DB_HOST": Variable.get("DB_HOST"),
            "DB_PORT": Variable.get("DB_PORT"),
            "DB_PASS": Variable.get("DB_PASS"),
            "DB_NAME": Variable.get("DB_NAME"),
            "DB_USER": Variable.get("DB_USER"),
        },
    )

    rmq_sensor >> import_1c
