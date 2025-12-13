import logging.config

import yaml
from adaptix import Retort, name_mapping, NameStyle
from adaptix.conversion import impl_converter

from app.models.config import Config
from app.models.config.main import _Config
from app.models.config.main import Paths

logger = logging.getLogger(__name__)

retort = Retort(recipe=[
    name_mapping(name_style=NameStyle.LOWER_KEBAB)
])

def load_config(paths: Paths) -> Config:
    with (paths.config_path / "config.yaml").open("r") as f:
        config_dct = yaml.safe_load(f)
    loaded_config = retort.load(config_dct, _Config)
    return make_config(loaded_config, paths)


@impl_converter
def make_config(config: _Config, paths: Paths) -> Config:
    pass
