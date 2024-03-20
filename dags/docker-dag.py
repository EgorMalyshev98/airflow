from datetime import datetime

from airflow import DAG

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable


with DAG(
    dag_id="zhufwr_import",
    start_date=datetime(2023, 12, 12),
    catchup=False,
    tags=["dbt", "1c"],
    schedule=None,
) as dag:
    
    import_1c = DockerOperator(
        task_id="rmq_to_postgres",
        # image="af_1c_task:1",
        image="busybox",
        api_version="auto",
        command = ["printenv"],
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        auto_remove="success",
        environment = {
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
            "DB_USER": Variable.get("DB_USER")
        }   
    )

    import_1c