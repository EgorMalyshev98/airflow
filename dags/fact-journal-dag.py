from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models.baseoperator import chain
from airflow.models.variable import Variable
from pendulum import datetime

from plugins.notifiers.tg_notifier import TelegramNotification
from plugins.sensors.rmq_sensor import RMQSensor


default_args = {
    "on_failure_callback": TelegramNotification(
        telegram_bot_token=Variable.get("tg_bot_token"),
        telegram_chat_id=Variable.get("alerting_chat_id"),
    )
}


@dag(
    start_date=datetime(2025, 4, 2),
    end_date=None,
    catchup=False,
    doc_md=__doc__,
    schedule=None,
    max_consecutive_failed_dag_runs=5,
    on_failure_callback=None,
    on_success_callback=None,
    default_args=default_args,
    tags=['1c', 'dbt', 'dwh']
)

def journal_1c_dag():
    """1c ЖУФВР ETL
    """
    rabbit_sensor = RMQSensor(
        task_id="rabbit_journal_sensor_task",
        rmq_conn_id="1c_rmq_dev",
        mode="reschedule",
        poke_interval=60 * 3,
        timeout=60 * 10 - 60,
        soft_fail=True,
        wait_for_downstream=True,
    )

    rabbit_consumer = DockerOperator(
        task_id='rabbit_journal_consumer_task',
        image='tsm-dwh-consumer:1',
        api_version='auto',
        command='dbt build',
        environment=
        {
            'DBT_HOST': '172.17.0.1'
        },
        mem_limit='1g',
        # network_mode='brige',
        auto_remove='success'
    )
    
    dbt_run = DockerOperator(
        task_id='second_task',
        image='tsm-dwh-dbt:1',
        api_version='auto',
        command='dbt build',
        environment=
        {
            'DBT_HOST': '172.17.0.1'
        },
        mem_limit='1g',
        # network_mode='brige',
        auto_remove='success'
    )
    
    rabbit_sensor >> rabbit_consumer >> dbt_run
    
    
journal_1c_dag()







