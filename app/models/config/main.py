from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    app_dir: Path
