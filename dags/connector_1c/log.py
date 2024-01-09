from loguru import logger
from pathlib import Path

def setup_logger():
    log_path = Path(__file__).parent.parent / 'app_logs'
    
    logger.add(log_path.joinpath("logs.log"), rotation='50 MB')
    logger.add(log_path.joinpath("info.log"),
        filter=lambda record: record["level"].name == "INFO", rotation='50 MB')
    # logger.add(log_path.joinpath("failed_rmq_messages.json"),
    #     filter=lambda record: record["level"].name == "RMQ", rotation='100 MB', serialize=True)
    logger.add(log_path.joinpath("errors.log"),
        filter=lambda record: record["level"].name == "ERROR", rotation='50 MB')
    logger.add(log_path.joinpath("debug.log"),
        filter=lambda record: record["level"].name == "DEBUG", rotation='10 MB')
    
    return logger

app_logger = setup_logger()