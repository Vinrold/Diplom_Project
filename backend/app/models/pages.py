from sqlalchemy import Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Pages(Base):
    # Указание таблицы БД
    __tablename__ = "pages"
    #  уникальность сочетаний comics_id, chapters_id, number
    __table_args__ = (
        UniqueConstraint(
            "comics_id", "chapters_id", "number", name="uq_pages_uq_number"
        ),
    )

    # Указываем столбцы
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Номер картинки
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    # сылка на ИД комикса
    comics_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("comics.id", ondelete="CASCADE"),
        nullable=False
    )

    # Ссылка на ИД  
    chapters_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=False
    )

    # Ссылка на изображение на сервере.
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)

    # Связь изображения с комиксом и главой (Для выборки)
    comic: Mapped["Comics"] = relationship(back_populates="pages")
    chapter: Mapped["Chapters"] = relationship(back_populates="pages")