from pydantic import BaseModel, ConfigDict, EmailStr, Field

# класс для описания, какие данные будут отправлять от клиента
class UserCreate(BaseModel):
    # id - генерируется самой БД, поэтому сайт его не отправляет
    nickname: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

# логин и пароль для входа
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ответ с токенном доступа
class Token(BaseModel):
    access_token: str
    token_type: str


# класс для описания, что в ответ должен отправить на сайт сервер
class UserResponse(BaseModel):
    # сервер узнает от БД, какой id получил пользователь
    id: int
    nickname: str
    email: str
    # пароль для безопасности сервер не отправляет обратно

    # чтобы Пайдентик мог читать данные не только от SQL ответа, но и из
    # объектов SQLalchemy orm
    model_config = ConfigDict(from_attributes=True)