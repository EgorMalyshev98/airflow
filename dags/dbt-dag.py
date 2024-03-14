from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


from dbt_airflow.core.config import DbtAirflowConfig, DbtProjectConfig, DbtProfileConfig
from dbt_airflow.core.task_group import DbtTaskGroup
from dbt_airflow.core.task import ExtraTask
from dbt_airflow.operators.execution import ExecutionOperator
from dbt_airflow.operators.bash import DbtBaseOperator


with DAG(
    dag_id='dbt_airflow_dag',
    start_date=datetime(2023, 12, 12),
    catchup=False,
    tags=['dbt'],
) as dag:

    extra_tasks = [
        # ExtraTask(
        #     task_id='test_task',
        #     operator=DbtBaseOperator(dbt_base_command='dbt debug'),
        #     # operator_args={
        #     #     'dbt': lambda: print('Hello world'),
        #     # },
        #     # upstream_task_ids={
        #     #     'model.example_dbt_project.int_customers_per_store',
        #     #     'model.example_dbt_project.int_revenue_by_date'
        #     # }
        # )
        # ExtraTask(
        #     task_id='test_task',
        #     operator=PythonOperator,
        #     operator_args={
        #         'python_callable': lambda: print('Hello world'),
        #     },
        #     upstream_task_ids={
        #         'model.example_dbt_project.int_customers_per_store',
        #         'model.example_dbt_project.int_revenue_by_date'
        #     }
        # ),
        # ExtraTask(
        #     task_id='another_test_task',
        #     operator=PythonOperator,
        #     operator_args={
        #         'python_callable': lambda: print('Hello world 2!'),
        #     },
        #     upstream_task_ids={
        #         'test.example_dbt_project.int_customers_per_store',
        #     },
        #     downstream_task_ids={
        #         'snapshot.example_dbt_project.int_customers_per_store_snapshot',
        #     }
        # ),
        # ExtraTask(
        #     task_id='test_task_3',
        #     operator=PythonOperator,
        #     operator_args={
        #         'python_callable': lambda: print('Hello world 3!'),
        #     },
        #     downstream_task_ids={
        #         'snapshot.example_dbt_project.int_customers_per_store_snapshot',
        #     },
        #     upstream_task_ids={
        #         'model.example_dbt_project.int_revenue_by_date',
        #     },
        # )
    ]

    t1 = EmptyOperator(task_id='empty_1')
    t2 = EmptyOperator(task_id='empty_2')

    tg = DbtTaskGroup(
        group_id='dbt-company',
        dbt_project_config=DbtProjectConfig(
            project_path=Path('/opt/airflow/dags/oup_dbt/'),
            manifest_path=Path('/opt/airflow/dags/oup_dbt/target/manifest.json'),
        ),
        dbt_profile_config=DbtProfileConfig(
            profiles_path=Path('/opt/airflow/dags/oup_dbt/.dbt/'),
            target='prod',
        ),
        dbt_airflow_config=DbtAirflowConfig(
            extra_tasks=extra_tasks,
            execution_operator=ExecutionOperator.BASH,
            # select=['tag:daily'],
            # exclude=['*'],
            full_refresh=True,
            # variables='{key: value, date: 20190101}',
            no_partial_parse=True,
        )
    )

    t1 >> tg >> t2
