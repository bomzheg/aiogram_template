from sqlalchemy.orm import mapped_column, Mapped

from app.models import dto
from app.models.db.base import Base


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str]
    is_bot: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        rez = (
            f"<User "
            f"ID={self.tg_id} "
            f"name={self.first_name} {self.last_name} "
        )
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
