from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Genres_comicses(Base):
    # Указание таблицы БД
    __tablename__ = "genres_comics"

    # Составной первичный ключ
    # сылка на ИД комикса
    comics_id: Mapped[int] = mapped_column(
        ForeignKey("comics.id", ondelete="CASCADE"),
        primary_key=True
    )
    # Ссылка на Жанр
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True
    )