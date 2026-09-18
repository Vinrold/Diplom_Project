from sqlalchemy import Integer, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base


class Chapters(Base):
    # Указание таблицы БД
    __tablename__ = "chapters"

    # Указываем столбцы
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # сылка на ИД комикса
    comics_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("comics.id", ondelete="CASCADE"),
        nullable=False
    )

    # номер главы по счету
    number: Mapped[int] = mapped_column(Integer, nullable=False)


    # Название главы (не обязательно)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Дату публикации поставит сама БД
    publik_date: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )

    # Связь с скомисом
    comics: Mapped["Comics"] = relationship(back_populates="chapters")