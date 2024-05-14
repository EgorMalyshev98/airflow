from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models import Variable

from dbt_airflow.core.config import DbtAirflowConfig, DbtProjectConfig, DbtProfileConfig
from dbt_airflow.core.task_group import DbtTaskGroup
from dbt_airflow.core.task import ExtraTask
from dbt_airflow.operators.execution import ExecutionOperator
from dbt_airflow.operators.bash import DbtBashOperator

from notifiers.tg_notifier import TelegramNotification


project_path=Path('/opt/airflow/dags/oup_dbt/')
manifest_path=Path('/opt/airflow/dags/oup_dbt/target/manifest.json')
profiles_path=Path('/opt/airflow/dags/oup_dbt/.dbt/')

default_args = {
    "on_failure_callback": TelegramNotification(
        telegram_bot_token=Variable.get("tg_bot_token"),
        telegram_chat_id=Variable.get("alerting_chat_id"),
    )
}


with DAG(
    dag_id='dbt_airflow_dag',
    start_date=datetime(2023, 12, 12),
    catchup=False,
    tags=['dbt'],
    default_args=default_args
) as dag:
    
    t1 = EmptyOperator(task_id='empty_1')
    t2 = EmptyOperator(task_id='empty_2')
    
    extra_tasks = [
        ExtraTask(
            task_id='test_source',
            operator = DbtBashOperator,
            operator_args={
                "dbt_base_command": 'test -s "source:*" --exclude "test__mart__gant_archive_by_month", "test__duplication_of_oper"  ',
                "dbt_profile_path": profiles_path,
                "dbt_project_path": project_path,
                "dbt_target_profile": 'prod',
                "select": None,
                "exclude": None,
                "full_refresh": None,
                "no_write_json": None,
                "variables": None
            },
            downstream_task_ids={
                "model.oup_dbt.int__gant_start_transform",
                "model.oup_dbt.int__vdc_by_objects",
                "model.oup_dbt.int__archive_by_month"
            }
        )
    ]

    tg = DbtTaskGroup(
        group_id='dbt-company',
        dbt_project_config=DbtProjectConfig(
            project_path=project_path,
            manifest_path=manifest_path,
        ),
        dbt_profile_config=DbtProfileConfig(
            profiles_path=profiles_path,
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
