import pika
from typing import Dict, List
from os import environ as env
from dotenv import load_dotenv
from schemas import ZhufvrSchema
import json
import uuid


load_dotenv('.env')

MQ_HOST= env.get('MQ_HOST')
MQ_PORT= env.get('MQ_PORT')


def read_from_file(json_file_path) -> List[Dict]:
    """
    read json file
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
    
        data = json.load(file)
        
    return data

bad_zhufvr_id = uuid.uuid4()

def change_zhufvr_id(data, bad_zhufvr=False):
    """
    change uuids by zhufvr pydantic model
    """
    if bad_zhufvr:
        zhufvr_id = uuid.UUID('3418fb60-30ef-4df6-8015-11811a2b50ec')
    else:
        zhufvr_id = uuid.uuid4()
        
    work_id = uuid.uuid4()
    
    zhufvr = ZhufvrSchema(**data)
    
    zhufvr.value.link = zhufvr_id
    zhufvr.value.works[0].key_link = work_id
    zhufvr.value.materials[0].work_id = work_id
    zhufvr.value.pikets[0].key_link = work_id
    zhufvr.value.technique_workers[0].key_link = work_id
    zhufvr.value.norm_workload[0].key_link = work_id

    msg_body = zhufvr.model_dump_json(by_alias=True)

    return msg_body


#отправка сообщения в очередь
def send_message(queue: str, file_path, host='localhost'):
    """
    send message to RabbitMQ
    """
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    data = read_from_file(file_path)
    
    
    for _ in range(100000):
        body = change_zhufvr_id(data, bad_zhufvr=False)
        channel.basic_publish(exchange='',
                            routing_key=queue,
                            body=body)
    for _ in range(2):
        body = change_zhufvr_id(data, bad_zhufvr=True)
        channel.basic_publish(exchange='',
                            routing_key=queue,
                            body=body)
    for _ in range(100000):
        body = change_zhufvr_id(data, bad_zhufvr=False)
        channel.basic_publish(exchange='',
                            routing_key=queue,
                            body=body)

    connection.close()



if __name__=='__main__':
    import os
    
    path = os.path.join(os.path.pardir, os.path.pardir, os.getcwd())
    filename = '1c.json'
    
    file_path = os.path.join(path, filename)

    send_message(queue='oup', file_path=file_path)
