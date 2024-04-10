from logging.config import fileConfig
from sqlalchemy import pool
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import os
import sys
from pathlib import Path


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support

sys.path.append(os.path.join(sys.path[0], Path().resolve().parent))
from backend.src.database.models import Base
from backend.core.config import settings

target_metadata = Base.metadata
section = config.config_ini_section
config.set_section_option(section, 'SQLALCHEMY_DATABASE_URI', str(settings.SQLALCHEMY_DATABASE_URI))


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    """Run migrations in 'online' mode.
    """
    connectable = config.attributes.get("connection", None)

asyncio.run(run_async_migrations())
