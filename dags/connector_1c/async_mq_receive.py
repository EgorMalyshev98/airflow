import asyncio
import aiofiles
import json
import os
from aio_pika import connect, IncomingMessage
from dags.connector_1c.schemas import ZhufvrSchema
from database import get_async_session
from dags.connector_1c.converter import zhufvr_to_sql
from dags.connector_1c.models import Zhufvr
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from sqlalchemy import delete, select
from log import app_logger as logger
from pathlib import Path


class MessageProcessor:
    def __init__(self, session: AsyncSession, **kwargs):
        
        self.queue_name = kwargs.get('QUEUE')
        self.host = kwargs.get('MQ_HOST') 
        self.port = kwargs.get('MQ_PORT') 
        self.vhost = kwargs.get('MQ_VHOST') 
        self.mq_login = kwargs.get('MQ_LOGIN') 
        self.mq_pass = kwargs.get('MQ_PASS') 
        self.max_batch_size = kwargs.get('MAX_BATCH_SIZE') 
        self.msg_data = []
        self.tasks = []
        self.msg_counter = 0
        self.prefetch_count = 1000
        self.is_requeue = False
        self.session = session
        self.failed_msg_count = 0
        
        
    async def stop_receive(self):
        await self.connection.close()
        
        
    async def _save_json_to_file(self, data):
        
        path = Path(__file__).parent.parent.parent / f'app_logs'
        os.makedirs(path, exist_ok=True)
        filename = path.joinpath(f'{self.failed_msg_count}.json')
        async with aiofiles.open(filename, mode='w', encoding='utf-8') as file:
            json_data = json.dumps(data, indent=4, ensure_ascii=False)
            await file.write(json_data)
        
        
    async def _upsert_zhufvr(self):
        """" 
        delete and insert statement for load zhufvr models
        """
        sql_models = []
        zhufvr_id_lst = []
        
        for msg in self.msg_data:
            zhufvr = await zhufvr_to_sql(msg)
            id = zhufvr.link
            
            if id in zhufvr_id_lst:
                inx = zhufvr_id_lst.index(id)
                zhufvr_id_lst.pop(inx)
                sql_models.pop(inx)
                
            sql_models.append(zhufvr)
            zhufvr_id_lst.append(id)
                
        try: 
            
            select_query = select(Zhufvr.link).where(Zhufvr.link.in_(zhufvr_id_lst))
            duplicates_id = await self.session.scalars(select_query)
            id_lst = duplicates_id.all()
            logger.debug('select duplicates id')
            
            if id_lst:
                logger.debug(f'{len(id_lst)} duplicates')
                stmt = delete(Zhufvr).where(Zhufvr.link.in_(id_lst))
                logger.debug('start delete statment')
                await self.session.execute(stmt)
                logger.debug('delete statment executed')
            
            self.session.add_all(sql_models)
            await self.session.commit()
            logger.debug('loaded to db')
            
        except DBAPIError as e:
            logger.warning(e)
            self.session = await get_async_session()
            await self._upsert_zhufvr()
            logger.debug('session was updated')
            
        except Exception:
            raise
        
                            
    async def process_messages(self, message: IncomingMessage) -> None:
        """
        Process RabbitMQ messages

        Args:
            message (IncomingMessage)
        """
        try:
            await self._upsert_zhufvr()
            await message.ack(multiple=True)

        except Exception as e:
            await message.nack(multiple=True, requeue=True) #for debug
            logger.error(e)


    async def on_message(self, message: IncomingMessage) -> None:
        
        async def start_process():
                await self.process_messages(message)
                current_queue = await self.channel.declare_queue(self.queue_name, durable=True)
                self.len_queue = current_queue.declaration_result.message_count
                self.batch_size = min(self.max_batch_size, self.len_queue)
                if not self.len_queue:
                    self.is_requeue = True
                self.msg_data = []
                self.msg_counter = 0
                
        try:
            data = json.loads(message.body)
            self.msg_data.append(ZhufvrSchema(**data))
            self.msg_counter += 1
            
            if self.msg_counter >= self.batch_size:
                logger.debug('start process normally')
                await start_process()
                
            
        except ValidationError as e:
            logger.error(f'Pydantic validation err: {e}')
            logger.debug('validation err')
            await self._save_json_to_file(data)
            self.failed_msg_count += 1
            logger.debug('message logged')
            
            if self.msg_data:
                logger.debug('start process after Validation Err')
                await start_process()
                
        except UnicodeDecodeError:
            logger.error(f'invalid message: \n{message.info}')
            
            if self.msg_data:
                await start_process()
                logger.debug('process after Validation Err')
                
            logger.debug('reject message after UnicodeDecodeError error')
                        
                        
    async def receive(self):
        self.loop  = asyncio.get_running_loop()
        self.connection = await connect(host=self.host, 
                                        port=self.port,
                                        login=self.mq_login,
                                        password=self.mq_pass,
                                        virtualhost=self.vhost,
                                        loop=self.loop)
        
    
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=self.prefetch_count)
        self.queue = await self.channel.declare_queue(name=self.queue_name, durable=True)
        self.len_queue = self.queue.declaration_result.message_count
        
        if not self.len_queue:
            return
                    
        self.batch_size = min(self.max_batch_size, self.len_queue)

        print(" [*] Waiting for logs. To exit press CTRL+C")
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                if self.is_requeue:
                    await self.connection.close()
                    self.is_requeue = False
                    #restart connection for requeue unack messages and update batch_size
                    await self.receive()
                await self.on_message(message)



