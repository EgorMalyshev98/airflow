from typing import Any, Dict
from airflow.providers.telegram.hooks.telegram import TelegramHook

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from airflow.models import Connection


import pika

from  loguru import logger
import pika.connection


class RMQHook(BaseHook):
    """
    Return RabbitMQ hook
    
    :param rmq_url: RabbitMQ URL string
    :return: RMQHook object
    """
    
    def __init__(
        self,
        rmq_url: str | None = None,
        *args, **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self.connection = pika.BlockingConnection(pika.connection.URLParameters(rmq_url))
        
        logger.info('Connected to RabbitMQ')
        
        
    
    def len_queue(self, queue: str):
        
        channel = self.connection.channel()
        queue_info = channel.queue_declare(queue=queue, durable=True)
        msg_count = queue_info.method.message_count
        
        return msg_count
    
