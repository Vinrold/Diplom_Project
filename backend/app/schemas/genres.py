from pydantic import BaseModel, ConfigDict
from typing import Optional

# создание Жанра
class GenreCreate(BaseModel):
    # id - генерируется самой БД, поэтому сайт его не отправляет
    name: str

# Обновление Жанра
class GenreUpdate(BaseModel):
    name: Optional[str] = None


# ответ сервера на сайт
class GenreResponse(BaseModel):
    # сервер узнает от БД, какой id получил пользователь
    id: int
    name: str

    # Для конвертации из модели алхимии 
    model_config = ConfigDict(from_attributes=True)