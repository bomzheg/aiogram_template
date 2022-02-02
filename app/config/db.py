from pathlib import Path

import yaml

from app.models.config.db import DBConfig


def load_db_config(config_path: Path) -> DBConfig:
    with (config_path / "db.yaml").open("r") as f:
        db_dict = yaml.safe_load(f)
    return DBConfig(
        type=db_dict.get('type', None),
        connector=db_dict.get('connector', None),
        host=db_dict.get('host', None),
        port=db_dict.get('port', None),
        login=db_dict.get('login', None),
        password=db_dict.get('password', None),
        name=db_dict.get('name', None),
        path=db_dict.get('path', None),
    )
