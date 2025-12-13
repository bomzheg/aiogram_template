import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DBConfig:
    type: str
    connector: str
    host: str
    port: int
    login: str
    password: str
    name: str
    path: str
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


@dataclass
class RedisConfig:
    url: str
    port: int = 6379
    db: int = 1
