from sqlalchemy import BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.chat_type import ChatType
from app.models import dto
from app.models.db.base import Base


class Chat(Base):
    __tablename__ = "chats"
    __mapper_args__ = {"eager_defaults": True}  # noqa: RUF012
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    type: Mapped[ChatType] = mapped_column(Enum(ChatType))
    title: Mapped[str]
    username: Mapped[str | None]

    def __repr__(self) -> str:
        rez = f"<Chat ID={self.tg_id} title={self.title} "
        if self.username:
            rez += f"username=@{self.username}"
        return rez + ">"

    def to_dto(self) -> dto.Chat:
        return dto.Chat(
            db_id=self.id,
            tg_id=self.tg_id,
            type=self.type,
            title=self.title,
            username=self.username,
        )
