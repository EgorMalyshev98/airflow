import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from sensors.rmq_sensor import RMQSensor
from notifiers.tg_notifier import TelegramNotification
from airflow.models import Variable

def process_task():
    time.sleep(3)
    
def fail():
    print(Variable.get("alerting_chat_id"))
    raise
    
default_args = {
    "on_failure_callback": TelegramNotification(
        telegram_bot_token=Variable.get("tg_bot_token"),
        telegram_chat_id=Variable.get("alerting_chat_id"))
}
    
with DAG(
    dag_id='rmq_sensor_dag',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['rmq', 'dbt'],
    schedule_interval=timedelta(hours=1),
    default_args=default_args
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
    
    rmq_sensor >> process_messages >> fail_task
    