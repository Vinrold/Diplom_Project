from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped, mapped_column
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
