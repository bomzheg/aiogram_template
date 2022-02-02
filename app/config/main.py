import logging.config
from pathlib import Path

from dotenv import load_dotenv

from app.config.db import load_db_config
from app.config.logging_config import setup_logging
from app.models.config import Config
from app.models.config.main import Paths

logger = logging.getLogger(__name__)


def load_config(app_dir: Path) -> Config:
    paths = Paths(app_dir)

    load_dotenv(paths.app_dir / ".env")
    setup_logging(paths)
    return Config(
        paths=paths,
        db=load_db_config(paths.config_path),
    )
