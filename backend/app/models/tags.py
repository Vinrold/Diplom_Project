from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Tags(Base):
    # Таблица с тэгами
    __tablename__ = "tags"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # наименование тэга 
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    comics: Mapped[list["Comics"]] = relationship(
        secondary="tag_comics",
        back_populates="tags",
    )
