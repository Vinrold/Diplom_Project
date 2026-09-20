from pydantic import BaseModel, ConfigDict
from typing import Optional

# создание картинки комикса
class PageCreate(BaseModel):
    # id - генерируется самой БД, поэтому сайт его не отправляет
    number: int
    comics_id: int
    chapters_id: int
    image_url: str

# Обновление картинки
class PageUpdate(BaseModel):
    number: Optional[int] = None
    image_url: Optional[str] = None


# ответ сервера на сайт
class PageResponse(BaseModel):
    # сервер узнает от БД, какой id получил пользователь
    id: int
    number: int
    comics_id: int
    chapters_id: int
    image_url: str

    # Для конвертации из модели алхимии 
    model_config = ConfigDict(from_attributes=True)