import logging.config
from pathlib import Path

import yaml
from contextlib import suppress

from app.models.config.main import Paths

logger = logging.getLogger(__name__)


def setup_logging(paths: Paths):
    with paths.logging_config_file.open("r") as f:
        logging_config = yaml.safe_load(f)
        with suppress(KeyError):
            log_dir = paths.log_path
            patch_filename(logging_config['handlers']['file'], log_dir)
            log_dir.mkdir(exist_ok=True)
        logging.config.dictConfig(logging_config)
    logger.info("Logging configured successfully")


def patch_filename(dct: dict, log_dir: Path):
    dct["filename"] = log_dir / dct["filename"]
