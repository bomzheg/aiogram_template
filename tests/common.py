import logging
from pathlib import Path

from alembic.config import Config as AlembicConfig

from app.config import load_config
from app.config.logging_config import setup_logging
from app.models.config import Config
from app.models.config.main import Paths

app_dir = Path(__file__).parent.parent
tests_dir = app_dir / "tests"


def create_alembic_config() -> AlembicConfig:
    app_config = create_app_config()
    # Create Alembic configuration object
    # (we don't need database for getting revisions list)
    config_name = app_config.config_path / "alembic.ini"
    config = AlembicConfig(file_=str(config_name))
    return config


def create_app_config() -> Config:
    paths = Paths(tests_dir)
    setup_logging(paths)
    return load_config(paths)


def create_test_container():
    import sqlalchemy
    from testcontainers.mysql import MySqlContainer

    with MySqlContainer('mysql:5.7.17') as mysql:
        engine = sqlalchemy.create_engine(mysql.get_connection_url())
        version, = engine.execute("select version()").fetchone()
        print(version)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    create_test_container()
