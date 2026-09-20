from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# создание коммента
class CommentCreate(BaseModel):
    # id - генерируется самой БД, поэтому сайт его не отправляет
    user_id: int
    comics_id: int
    content: str

# Обновление комента
class CommentUpdate(BaseModel):
    content: Optional[str] = None


# ответ сервера на сайт
class CommentResponse(BaseModel):
    # сервер узнает от БД, какой id получил пользователь
    id: int
    user_id: int
    comics_id: int
    content: str
    created_date: datetime

    # Для конвертации из модели алхимии 
    model_config = ConfigDict(from_attributes=True)

