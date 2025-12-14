from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    db_id: int | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_bot: bool | None = None
