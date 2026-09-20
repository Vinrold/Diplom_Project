from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# создание главы
class ChapterCreate(BaseModel):
    # id - генерируется самой БД, поэтому сайт его не отправляет
    comics_id: int
    number: int
    title: Optional[str] = None

# Обновление главы
class ChapterUpdate(BaseModel):
    number: Optional[int] = None
    title: Optional[str] = None


# ответ сервера на сайт
class ChapterResponse(BaseModel):
    # сервер узнает от БД, какой id получил пользователь
    id: int
    comics_id: int
    number: int
    title: Optional[str] = None
    publik_date: datetime

    # Для конвертации из модели алхимии 
    model_config = ConfigDict(from_attributes=True)


