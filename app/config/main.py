import logging.config
from pathlib import Path

from dotenv import load_dotenv

from app.config.logging_config import setup_logging
from app.models.config import Config


logger = logging.getLogger(__name__)


def load_config(app_dir: Path) -> Config:
    load_dotenv(app_dir / ".env")
    setup_logging(app_dir)
    return Config(
        app_dir=app_dir,
    )
