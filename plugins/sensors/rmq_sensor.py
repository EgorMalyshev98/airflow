from datetime import timedelta
from airflow.sensors.base import BaseSensorOperator
from loguru import logger


from hooks.rmq_hook import RMQHook

class RMQSensor(BaseSensorOperator):
    """
    RabbitMQ sensor
    
    :param rmq_conn_id: RabbitMQ connection id from airflows connections
    :param params: dict connection params:
    :return: RMQSensor object
    """
    def __init__(
            self, *, 
            rmq_queue: str,
            rmq_url: str,
            poke_interval: timedelta | float = 60, 
            timeout: timedelta | float = ..., 
            soft_fail: bool = False, 
            mode: str = "poke", 
            exponential_backoff: bool = False, 
            max_wait: timedelta | float | None = None, 
            silent_fail: bool = False,
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
            self.rmq_url = rmq_url
            self.rmq_queue = rmq_queue
            
    def poke(self, context):
        rmq_hook = RMQHook(self.rmq_url)
        msg_count = rmq_hook.len_queue(self.rmq_queue)
        logger.info(f'Message count: {msg_count}')
        print(f'Message count: {msg_count}')

        
        if msg_count:
            return True
        
        return False
        
