from pydantic import BaseModel, ConfigDict

# класс для описания, какие данные будут отправлять от клиента
class UserCreate(BaseModel):
    # id - генерируется самой БД, поэтому сайт его не отправляет
    nickname: str
    password: str

# класс для описания, что в ответ должен отправить на сайт сервер
class UserResponse(BaseModel):
    # сервер узнает от БД, какой id получил пользователь
    id: int
    nickname: str
    # пароль для безопасности сервер не отправляет обратно

    # чтобы Пайдентик мог читать данные не только от SQL ответа, но и из
    # объектов SQLalchemy orm
    model_config = ConfigDict(from_attributes=True)