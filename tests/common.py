from pathlib import Path

from alembic.config import Config

from app.config.db import load_db_config


app_dir = Path(__file__).parent.parent


def create_alembic_config() -> Config:
    # Create Alembic configuration object
    # (we don't need database for getting revisions list)
    config_name = app_dir / "alembic.ini"
    config = Config(file_=str(config_name))
    db_config = create_db_config()
    config.set_main_option("sqlalchemy.url", db_config.uri)
    config.set_main_option("script_location", str(app_dir / "migrations"))
    return config


def create_db_config():
    db_config = load_db_config(app_dir / "config")
    db_config.name = "daily_tests"
    return db_config
