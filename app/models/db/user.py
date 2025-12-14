from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models import dto
from app.models.db.base import Base


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}  # noqa: RUF012
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    is_bot: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        rez = f"<User ID={self.tg_id} name={self.first_name} {self.last_name} "
        if self.username:
            rez += f"username=@{self.username}"
        return rez + ">"

    def to_dto(self) -> dto.User:
        return dto.User(
            db_id=self.id,
            tg_id=self.tg_id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            is_bot=self.is_bot,
        )
