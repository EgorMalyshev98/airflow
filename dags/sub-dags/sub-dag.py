from asyncio import tasks
from datetime import datetime
from pathlib import Path
import select

from airflow import DAG

from dbt_airflow.operators.bash import DbtBashOperator
from marshmallow import EXCLUDE


with DAG(
    dag_id='sub-dag',
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['sub-example'],
) as dag:
    
    project_path=Path('/opt/airflow/dags/oup_dbt/')
    manifest_path=Path('/opt/airflow/dags/oup_dbt/target/manifest.json')
    profiles_path=Path('/opt/airflow/dags/oup_dbt/')
    
    t1 = DbtBashOperator(
        task_id = 'task_12422',
        dbt_base_command='build',
        dbt_profile_path=profiles_path,
        dbt_project_path=project_path,
        dbt_target_profile='prod',
        select = None,
        exclude = None,
        full_refresh = None,
        no_write_json = None,
        variables = None
    )

    t1
