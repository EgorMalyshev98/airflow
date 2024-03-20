from typing import Any, Dict
from airflow.providers.telegram.hooks.telegram import TelegramHook

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook

import pika
from pika import URLParameters


class RMQHook(BaseHook):
    """
    Return RabbitMQ hook
    
    Create hook
    rmq_hook = RabbitMQ(rmq_conn_id="rmq_conn_id")
    or rmq_hook = RabbitMQ(params=params)
    
    :param rmq_conn_id: RabbitMQ connection id from airflows connections
    :param params: dict connection params:
        {
            host: localhost
            virtual_host: None
            port: 5672
            login: None
            password: None
            queue: None
            heartbeat: None
        }
    :return: RMQHook object
    """
    
    def __init__(
        self,
        rmq_conn_id: str | None = None,
        params: dict | None = None,
        *args, **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self._conn_params: Dict = self.__get_rmq_conn_params(params, rmq_conn_id)
        self.connection: pika.BlockingConnection = self.get_conn()
    
    def __get_rmq_conn_params(self, params, rmq_conn_id):
        """
        :param rmq_conn_id: RabbitMQ connection id from airflows connections
        :param params: dict connection params:
        """
        
        if rmq_conn_id:
            conn = self.get_connection(rmq_conn_id)
            extra = conn.extra_dejson
            url = f"amqp://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}?heartbeat={extra['heartbeat']}"
            queue = extra["queue"]
            print(url)
            
        return {"url": URLParameters(url), "queue": queue}
            
            
    def get_conn(self) -> Any:
        """
        :return: RabbitMQ connection object
        """
        connection = pika.BlockingConnection(parameters=self._conn_params["url"])
        
        return connection
    
    def len_queue(self, queue=None):
        
        channel = self.connection.channel()
        if not queue:
            queue = self._conn_params["queue"]
            
        queue_info = channel.queue_declare(queue=queue, durable=True)
        msg_count = queue_info.method.message_count
        
        return msg_count
    
