from pathlib import Path
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.docker.operators.docker_swarm import DockerSwarmOperator
from notifiers.tg_notifier import TelegramNotification
from sensors.rmq_sensor import RMQSensor
from airflow import DAG
from airflow.models.variable import Variable

# from dbt_airflow.core.config import DbtAirflowConfig, DbtProjectConfig, DbtProfileConfig
# from dbt_airflow.core.task_group import DbtTaskGroup
# from dbt_airflow.core.task import ExtraTask
# from dbt_airflow.operators.execution import ExecutionOperator
# from dbt_airflow.operators.bash import DbtBashOperator


# default_args = {
#     "on_failure_callback": TelegramNotification(
#         telegram_bot_token=Variable.get("tg_bot_token"),
#         telegram_chat_id=Variable.get("alerting_chat_id"),
#     )
# }

project_path=Path('/opt/airflow/dags/oup_dbt/')
manifest_path=Path('/opt/airflow/dags/oup_dbt/target/manifest.json')
profiles_path=Path('/opt/airflow/dags/oup_dbt/.dbt/')


with DAG(
    dag_id="1c",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["rmq", "dbt", "2c"],
    schedule_interval=None,
    # default_args=default_args,``
    description="extract files from 1c RabbitMQ queue to postgres DWH"
) as dag:
    
    rmq_sensor = RMQSensor(
        task_id="rmq_task_sensor",
        rmg_url=Variable.get(''),
        mode="reschedule",
        poke_interval=60 * 3,
        timeout=60 * 10 - 60,
        soft_fail=True,
        wait_for_downstream=True,
    )

    import_1c = DockerSwarmOperator(
        task_id="rmq_to_postgres",
        image="af_1c_task:1",
        api_version="auto",
        docker_url="unix://var/run/docker.sock",
        networks=["bridge", "superset_superset"],
        # auto_remove=True,
        environment={
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
            "DB_USER": Variable.get("DB_USER"),
        },
    )
    
    # #dbt tasks:
    # extra_tasks = [
    #     ExtraTask(
    #         task_id='test_source_1C',
    #         operator = DbtBashOperator,
    #         operator_args={
    #             "dbt_base_command": 'test -s "+mart_1C", "source:*" --exclude "test__mart__gant_archive_by_month", "test__duplication_of_oper"',
    #             "dbt_profile_path": profiles_path,
    #             "dbt_project_path": project_path,
    #             "dbt_target_profile": 'prod',
    #             "select": None,
    #             "exclude": None,
    #             "full_refresh": None,
    #             "no_write_json": None,
    #             "variables": None
    #         },
    #         downstream_task_ids={
    #             "model.oup_dbt.int__gant_start_transform",
    #             "model.oup_dbt.int__vdc_by_objects",
    #             "model.oup_dbt.int__archive_by_month"
    #         }
    #     )
    # ]

    # dbt_tasks = DbtTaskGroup(
    #     group_id='dbt-1c',
    #     dbt_project_config=DbtProjectConfig(
    #         project_path=project_path,
    #         manifest_path=manifest_path,
    #     ),
    #     dbt_profile_config=DbtProfileConfig(
    #         profiles_path=profiles_path,
    #         target='prod',
    #     ),
    #     dbt_airflow_config=DbtAirflowConfig(
    #         extra_tasks=extra_tasks,
    #         execution_operator=ExecutionOperator.BASH,
    #         # select=["+mart_1C"],
    #         # exclude=['*'],
    #         full_refresh=True,
    #         # variables='{key: value, date: 20190101}',
    #         no_partial_parse=True,
    #     )
    # )

    rmq_sensor >> import_1c 
    # >> dbt_tasks
    
