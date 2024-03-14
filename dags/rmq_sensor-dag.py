import time
from datetime import datetime, timedelta

from airflow import DAG
from scripts.rmq_sensor import RMQSensor


with DAG(
    dag_id='rmq_sensor_dag',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['rmq', 'dbt'],
    schedule_interval=None
) as dag:
    
    rmq_sensor = RMQSensor(
        task_id="rmq_task_1",
        rmq_conn_id="1c_rmq_dev",
        mode="poke",
        poke_interval=10,
        timeout=10*3)
    
    rmq_sensor
    