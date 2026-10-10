from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

# на основе Base создаются все модели в проекте
class User(Base):
    # указание имени таблицы для БД
    # в Пайтоне - коллекция объектов класса User
    # в постре - таблица users
    __tablename__ = "users"

    # указываются столбцы таблицы как поля объекта

    # - primary key - значение в столбце должно быть разным в каждой строке
    # таблицы для поиска конкретного пользователя
    # - autoincrement - БД сама будет считать каждый следующий id
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    comments: Mapped[list["app.models.comments.Comments"]] = relationship(back_populates="user", cascade="all, delete-orphan")