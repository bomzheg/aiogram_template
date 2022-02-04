from pathlib import Path

from alembic.config import Config

app_dir = Path(__file__).parent.parent


def create_alembic_config() -> Config:
    # Create Alembic configuration object
    # (we don't need database for getting revisions list)
    config_name = app_dir / "alembic.ini"
    config = Config(file_=str(config_name))
    config.set_main_option("sqlalchemy.url", "postgresql+asyncpg://postgres:postgres@localhost:5432/daily_test")
    config.set_main_option("script_location", str(app_dir / "migrations"))
    return config

