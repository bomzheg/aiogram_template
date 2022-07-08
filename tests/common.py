from pathlib import Path

from alembic.config import Config as AlembicConfig

from app.config import load_config
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
    return load_config(Paths(tests_dir))
