from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# создание комикса
class ComicsCreate(BaseModel):
    # id - генерируется самой БД, поэтому сайт его не отправляет
    name: str
    description: Optional[str] = None

# Обновление комикса
class ComicsUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class GenreShots(BaseModel):
    id: int
    name: str


class TagShots(BaseModel):
    id: int
    name: str


# ответ сервера на сайт
class ComicsResponse(BaseModel):
    # сервер узнает от БД, какой id получил комикс
    id: int
    name: str
    description: Optional[str] = None
    genres: List[GenreShots] = []
    tags: List[TagShots] = []

    # Для конвертации из модели алхимии
    model_config = ConfigDict(from_attributes=True)


 
