import asyncio
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine

from app.config.db import load_db_config
from app.models.config.db import DBConfig
from app.models.config.main import Paths
from app.models.db.base import Base


app_dir = Path(__file__).parent.parent
config = load_db_config(Paths(app_dir).config_path)
target_metadata = Base.metadata


def run_migrations_offline(db_config: DBConfig):
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=db_config.uri,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online(db_config: DBConfig):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        create_engine(
            db_config.uri,
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline(config)
else:
    asyncio.run(run_migrations_online(config))
