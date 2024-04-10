import datetime
from typing import Annotated
from sqlalchemy import MetaData, func, String, BIGINT, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from contextlib import asynccontextmanager

from .config import settings


async_engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,
    echo=True
)

async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

bigint = Annotated[int, int]

created_at = Annotated[
    datetime.datetime, mapped_column(server_default=func.current_timestamp())
]


class Base(DeclarativeBase):

    metadata = MetaData(
        naming_convention=naming_convention
    )
    type_annotation_map = {
        bigint: BIGINT,
        datetime.datetime: TIMESTAMP(timezone=False),
    }
    created_at: Mapped[created_at]
    # updated_at: Mapped[updated_at]


@asynccontextmanager
async def db_session() -> AsyncSession:
    session = async_session()
    try:
        yield session
    # except (HTTPException, Exception):
    #     await session.rollback()
    finally:
        await session.close()
