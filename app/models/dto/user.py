from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
