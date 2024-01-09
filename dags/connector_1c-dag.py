from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator




with DAG(
    dag_id='test_dag',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['1c_connector'],
) as dag:
    
     pass


