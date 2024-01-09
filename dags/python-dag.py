from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task




with DAG(
    dag_id='python_dag',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['python-dag'],
) as dag:
    
    def _print_context(**context):
        start = context["execution_date"]
        end = context["next_execution_date"]
        print(f"Start: {start}, end: {end}")
        print(context)
        
    print_context = PythonOperator(
            task_id="print_context", python_callable=_print_context, dag=dag
            )
        
    
    print_context