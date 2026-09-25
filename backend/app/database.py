from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings
from pydantic_settings import BaseSettings

# создание движка для взаимодействия с БД
# ORM - мы пишем классы (модели), пайтон их переводит в SQL-запросы
# echo=True - выводит полученные запросы после перевода
engine = create_engine(settings.DATABASE_URL, echo=True)

# создание сессий (подключений) к БД
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# по правилам SQLalchemy все модели должны наследоваться от Base
# при этом он может быть и пустым
class Base(DeclarativeBase):
    pass