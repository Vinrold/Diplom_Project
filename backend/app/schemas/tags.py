from pydantic import BaseModel, ConfigDict
from typing import Optional

# создание Тэга
class TagCreate(BaseModel):
    # id - генерируется самой БД, поэтому сайт его не отправляет
    name: str

# Обновление Тэга
class TagUpdate(BaseModel):
    name: Optional[str] = None


# ответ сервера на сайт
class TagResponse(BaseModel):
    # сервер узнает от БД, какой id получил пользователь
    id: int
    name: str

    # Для конвертации из модели алхимии 
    model_config = ConfigDict(from_attributes=True)