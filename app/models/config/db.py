import logging
from dataclasses import dataclass
from typing import Protocol

logger = logging.getLogger(__name__)


class DBConfig(Protocol):
    echo: bool

    @property
    def uri(self) -> str:
        raise NotImplementedError


@dataclass(kw_only=True, frozen=True, slots=True)
class DBConfigProperties(DBConfig):
    type: str
    connector: str
    host: str
    port: int
    login: str
    password: str
    name: str
    path: str = ""
    echo: bool = False

    @property
    def uri(self) -> str:
        if self.type in ("mysql", "postgresql"):
            url = (
                f"{self.type}+{self.connector}://"
                f"{self.login}:{self.password}"
                f"@{self.host}:{self.port}/{self.name}"
            )
        elif self.type == "sqlite":
            url = f"{self.type}://{self.path}"
        else:
            raise ValueError("DB_TYPE not mysql, sqlite or postgres")
        logger.debug(url)
        return url


@dataclass(kw_only=True, frozen=True, slots=True)
class RedisConfig:
    url: str
    port: int = 6379
    db: int = 1
