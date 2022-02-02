import logging.config
from pathlib import Path

import yaml

from app.models.config.main import Paths

logger = logging.getLogger(__name__)


def setup_logging(paths: Paths):
    log_dir = paths.log_path
    log_dir.mkdir(exist_ok=True)
    with paths.logging_config_file.open("r") as f:
        logging_config = yaml.safe_load(f)
        patch_filename(logging_config['handlers']['file'], log_dir)
        logging.config.dictConfig(logging_config)
    logger.info("Logging configured successfully")


def patch_filename(dct: dict, log_dir: Path):
    dct["filename"] = log_dir / dct["filename"]
