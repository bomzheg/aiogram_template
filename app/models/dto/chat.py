from dataclasses import dataclass

from app.enums.chat_type import ChatType


@dataclass
class Chat:
    tg_id: int
    type: ChatType
    db_id: int | None = None
    username: str | None = None
    title: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    @property
    def full_name(self) -> str:
        name = ""
        if self.first_name:
            name += self.first_name + " "
        if self.last_name:
            name += self.last_name + " "
        if name == "":
            return str(self.tg_id)
        else:
            return name

    @property
    def name(self) -> str:
        if self.type == ChatType.private:
            return self.full_name
        return self.title or str(self.tg_id)
