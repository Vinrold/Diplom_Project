from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Comics(Base):
    # Указание таблицы БД
    __tablename__ = "comics"

    # Указываем столбцы
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # наименование сомикса
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # описание комикса
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # связь 
    chapters: Mapped[list["Chapters"]] = relationship(
        back_populates="comic",
        cascade="all, delete-orphan"
    )
    pages: Mapped[list["Pages"]] = relationship(
        back_populates="comic",
        cascade="all, delete-orphan"
    )
    tags: Mapped[list["Tags"]] = relationship(
        secondary="tag_comics",
        back_populates="comics",
    )