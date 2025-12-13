import logging.config

import yaml
from adaptix import Retort

from app.models.config import Config
from app.models.config.main import Paths

logger = logging.getLogger(__name__)

retort = Retort()

def load_config(paths: Paths) -> Config:
    with (paths.config_path / "config.yaml").open("r") as f:
        config_dct = yaml.safe_load(f)
    return retort.load(config_dct, Config)
