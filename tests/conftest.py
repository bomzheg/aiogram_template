from pathlib import Path

import pytest

from app.config.logging_config import setup_logging
from app.models.config.main import Paths, Config
from config.main import load_config


@pytest.fixture()
def app_config() -> Config:
    paths = Paths(Path(__file__).parent.parent / "tests")
    setup_logging(paths)
    return load_config(paths)
