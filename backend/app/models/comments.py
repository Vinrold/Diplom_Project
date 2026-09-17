from sqlalchemy import Integer, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base


class Comments(Base):
    # Указание таблицы БД
    __tablename__ = "comments"

    # Указываем столбцы
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # сылка на ИД юзера
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # сылка на ИД комикса
    comics_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("comics.id", ondelete="CASCADE"),
        nullable=False
    )

    # текст комментария
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Дату поставит сама БД
    created_date: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )