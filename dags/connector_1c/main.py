import asyncio
from dags.connector_1c.async_mq_receive import MessageProcessor
from config import processor_params, db_params
from database import get_async_session
from log import app_logger as logger


session = get_async_session()

def start_process():
    
    processor = MessageProcessor(session=session, **processor_params, **db_params)
    task = asyncio.create_task(processor.receive())

    asyncio.run(task)


            
    
    