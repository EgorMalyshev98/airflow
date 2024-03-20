from multiprocessing import process
import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from sensors.rmq_sensor import RMQSensor
from airflow.models import Variable

def process_task():
    time.sleep(3)
    
def fail():
    raise


with DAG(
    dag_id='rmq_sensor_dag',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['rmq', 'dbt'],
    schedule_interval=timedelta(hours=1)
) as dag:
    
    rmq_sensor = RMQSensor(
        task_id="rmq_task_1",
        rmq_conn_id="1c_rmq_dev",
        mode="poke",
        poke_interval=5,
        timeout=10*3,
        soft_fail=True,
        wait_for_downstream=True
        )
    
    process_messages = PythonOperator(
        task_id="process_messages",
        python_callable=process_task
    )
    
    fail_task = PythonOperator(
        task_id="fail_task",
        python_callable=fail
    )
    
    send_telegram_message = TelegramOperator(
        task_id="send_telegram_message",
        token=Variable.get("tg_bot_token"),
        chat_id=Variable.get("alerting_chat_id"),
        text="Уведомление Airflow"
    )
    rmq_sensor >> process_messages >> send_telegram_message
    