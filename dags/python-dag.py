import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.python import PythonSensor
from airflow.sensors.external_task import ExternalTaskSensor

default_args = {
    'depends_on_past': True
}

with DAG(
    dag_id='python_dag',
    default_args=default_args,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['python-dag', 'dbt'],
    schedule = timedelta(seconds=30)
) as dag:
    
    def process(**context):
        print('task processing')
        start = context["execution_date"]
        end = context["next_execution_date"]
        time.sleep(60 * 1)
        print(f"Start: {start}, end: {end}")
        
    def return_true():
        print('returned True')
        
        return True
    
    
    # Define the ExternalTaskSensor to wait for the completion of the previous run
    task_sensor = ExternalTaskSensor(
        task_id='wait_for_previous_run',
        external_dag_id='python_dag',
        external_task_id='processing_task',
        mode='poke',  # Change to 'reschedule' if you want it to wait and then resume on its own
        poke_interval=5,  # Time in seconds between checks
        timeout=30,  # Timeout for the sensor in seconds
        soft_fail=True
        # retries=1,  # Number of retries in case of sensor timeout
)
    
    python_sensor = PythonSensor(
        task_id="p_sensor",
        python_callable=return_true,
        poke_interval=5,
        timeout=60, #seconds
        soft_fail=True
        )
    
    print_context = PythonOperator(
            task_id="processing_task", python_callable=process, dag=dag
            )
        
    
    [python_sensor, task_sensor] >> print_context