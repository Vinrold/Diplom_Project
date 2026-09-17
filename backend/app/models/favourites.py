from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Favourites(Base):
    # Указание таблицы БД
    __tablename__ = "favourites"

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

    # ограничивает повторение пар user_id и comics_id для предотвращения добавления 
    # пользователем в избранное одного и того же комикса
    __table_args__ = (
        UniqueConstraint("user_id", "comics_id", name="unik_favorite_user_comics")
    )

