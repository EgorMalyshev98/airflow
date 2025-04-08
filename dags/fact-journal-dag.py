from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.docker.operators.docker_swarm import DockerSwarmOperator

from airflow.models.baseoperator import chain
from airflow.models.variable import Variable
from pendulum import datetime

from notifiers.tg_notifier import TelegramNotification
from sensors.rmq_sensor import RMQSensor


# default_args = {
#     "on_failure_callback": TelegramNotification(
#         telegram_bot_token=Variable.get("tg_bot_token"),
#         telegram_chat_id=Variable.get("alerting_chat_id"),
#     )
# }


@dag(
    dag_id='fact_journal_dag',
    start_date=datetime(2025, 4, 2),
    end_date=None,
    catchup=False,
    doc_md=__doc__,
    schedule=None,
    max_consecutive_failed_dag_runs=5,
    on_failure_callback=None,
    on_success_callback=None,
    # default_args=default_args,
    tags=['1c', 'dbt', 'dwh']
)
def journal_1c_dag():
    """1c ЖУФВР ETL
    """
    rabbit_sensor = RMQSensor(
        task_id="rabbit_journal_sensor_task",
        rmq_url=Variable.get('DEV_1C_MQ_URL'),
        rmq_queue=Variable.get('DEV_1C_QUEUE'),
        mode="reschedule",
        poke_interval=30,
        timeout=60 * 10 - 60,
        soft_fail=True,
        wait_for_downstream=False,
    )
    
    rabbit_consumer = DockerOperator(
        task_id='rabbit_journal_consumer_task',
        image='tsm-dwh-consumer:1',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        environment=
        {
            'DB_DNS': Variable.get('DWH_DB_DNS_SECRET'),
            'MQ_URL': Variable.get('DEV_1C_MQ_URL'),
            'QUEUE': Variable.get('DEV_1C_QUEUE'),
            'HEARTBEAT': 15,
        },
        # network_mode='brige',
        auto_remove='success'
    )
    
    dbt_run = DockerOperator(
        task_id='dbt_journal_task',
        image='tsm-dwh-dbt:1',
        api_version='auto',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        command='dbt build',
        environment=
        {
            'DBT_HOST': Variable.get('DBT_HOST_SECRET'),
            'DBT_PASS': Variable.get('DBT_PASS_SECRET'),
            'DBT_PORT': Variable.get('DBT_PORT'),
            'DBT_USER': Variable.get('DBT_USER')
        },
        # network_mode='brige',
        auto_remove='success'
    )
    
    rabbit_sensor >> rabbit_consumer >> dbt_run
    
    
journal_1c_dag()







