from dataclasses import dataclass

from app.enums.chat_type import ChatType


@dataclass
class Chat:
    id: int
    type: ChatType
    username: str | None = None
    title: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name or ""

    @property
    def name(self):
        if self.type == ChatType.private:
            return self.full_name
        return self.title
