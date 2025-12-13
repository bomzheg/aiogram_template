from dataclasses import dataclass

from app.models.config.db import DBConfig


@dataclass(kw_only=True)
class DBConfigMock(DBConfig):
    _uri: str
    echo: bool = False

    @property
    def uri(self) -> str:
        return self._uri
