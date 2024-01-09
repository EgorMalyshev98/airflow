from dotenv import load_dotenv
from os import environ as env

load_dotenv()

SECRET_AUTH = env.get('SECRET_AUTH')

processor_params = {
    'QUEUE': env.get('QUEUE'),
    'MQ_HOST': env.get('MQ_HOST'),
    'MQ_PORT': env.get('MQ_PORT'),
    'MQ_VHOST': env.get('MQ_VHOST'),
    'MQ_LOGIN': env.get('MQ_LOGIN'),
    'MQ_PASS': env.get('MQ_PASS'),
    'HEARTBEAT': env.get('HEARTBEAT'),
    'MAX_BATCH_SIZE': int(env.get('MAX_BATCH_SIZE'))
}

db_params = {
    'DB_HOST': env.get('DB_HOST'),
    'DB_PORT': env.get('DB_PORT'),
    'DB_PASS': env.get('DB_PASS'),
    'DB_NAME': env.get('DB_NAME'),
    'DB_USER': env.get('DB_USER'),
}
