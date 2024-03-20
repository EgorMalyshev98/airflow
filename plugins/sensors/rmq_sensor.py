from datetime import timedelta
from airflow.sensors.base import BaseSensorOperator

from hooks.rmq_hook import RMQHook

class RMQSensor(BaseSensorOperator):
    """
    RabbitMQ sensor
    
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
    :return: RMQSensor object
    """
    def __init__(
            self, *, 
            poke_interval: timedelta | float = 60, 
            timeout: timedelta | float = ..., 
            soft_fail: bool = False, 
            mode: str = "poke", 
            exponential_backoff: bool = False, 
            max_wait: timedelta | float | None = None, 
            silent_fail: bool = False,
            rmq_conn_id: str | None = None,
            conn_params: dict | None = None,
            **kwargs
            ) -> None:
        
            super().__init__(
                poke_interval=poke_interval, 
                timeout=timeout, 
                soft_fail=soft_fail, 
                mode=mode, 
                exponential_backoff=exponential_backoff, 
                max_wait=max_wait, 
                silent_fail=silent_fail, 
                **kwargs)
            self.rmq_conn_id = rmq_conn_id,
            self.conn_params = conn_params
            
            
    def poke(self, context):
        rmq_hook = RMQHook(self.rmq_conn_id)
        msg_count = rmq_hook.len_queue()
        print(f'Message count: {msg_count}')
        
        if msg_count:
            return True
        
        return False
        
