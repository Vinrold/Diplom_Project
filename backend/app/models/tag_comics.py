from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Tag_comics(Base):
    # Указание таблицы БД
    __tablename__ = "tag_comics"

    # Составной первичный ключ
    # сылка на ИД комикса
    comics_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("comics.id", ondelete="CASCADE"),
        primary_key=True
    )
    # Ссылка на Тэги
    tag_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True
    )