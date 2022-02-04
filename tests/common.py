from pathlib import Path

from alembic.config import Config

app_dir = Path(__file__).parent.parent


def create_alembic_config() -> Config:
    # Create Alembic configuration object
    # (we don't need database for getting revisions list)
    config_name = app_dir / "tests" / "config" / "alembic.ini"
    config = Config(file_=str(config_name))
    return config

