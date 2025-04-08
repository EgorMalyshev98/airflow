from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator
from airflow.models.variable import Variable
from pendulum import datetime

from notifiers.tg_notifier import TelegramNotification
from sensors.rmq_sensor import RMQSensor

from loguru import logger

# default_args = {
#     "on_failure_callback": TelegramNotification(
#         telegram_bot_token=Variable.get("tg_bot_token"),
#         telegram_chat_id=Variable.get("alerting_chat_id"),
#     )
# }


@dag(
    dag_id='sensor_test',
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
    """Тест сенсора rabbit
    """
    rabbit_sensor = RMQSensor(
        task_id="rabbit_journal_sensor_task",
        rmq_url=Variable.get('DEV_1C_MQ_URL'),
        rmq_queue=Variable.get('DEV_1C_QUEUE'),
        mode="reschedule",
        poke_interval=60 * 3,
        timeout=60 * 10 - 60,
        soft_fail=True,
        wait_for_downstream=True,
    )
    
    @task
    def task1():
        var = Variable.get('DEV_1C_MQ_URL')
        logger.debug(var)


    rabbit_sensor

journal_1c_dag()







