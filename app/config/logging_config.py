import logging.config
from pathlib import Path

import yaml


logger = logging.getLogger(__name__)


def setup_logging(app_dir: Path):
    log_dir = app_dir / "log"
    with (app_dir / "config" / "logging.yaml").open("r") as f:
        logging_config = yaml.safe_load(f)
        logging_config['handlers']['file']['filename'] = log_dir / "app.log"
        logging.config.dictConfig(logging_config)
    logger.info("Logging configured successfully")
