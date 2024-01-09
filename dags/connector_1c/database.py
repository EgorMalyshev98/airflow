from config import db_params
from typing import AsyncGenerator
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, registry, DeclarativeBase

url = f"postgresql+asyncpg://{db_params.get('DB_USER')}:{db_params.get('DB_PASS')}@{db_params.get('DB_HOST')}:{db_params.get('DB_PORT')}/{db_params.get('DB_NAME')}"

DATABASE_URL = url
Base = declarative_base()

convention = {
    "ix": "ix_%(column_0_label)s",  # INDEX
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",  # UNIQUE
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # CHECK
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",  # FOREIGN KEY
    "pk": "pk_%(table_name)s",  # PRIMARY KEY
}

mapper_registry = registry(metadata=MetaData(naming_convention=convention))

class BaseModel(DeclarativeBase):
    registry = mapper_registry
    metadata = mapper_registry.metadata
    

engine = create_async_engine(DATABASE_URL)
engine.echo = True
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
