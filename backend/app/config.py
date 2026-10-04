from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ''' 
    объект этого класса будет вытягивать все 
    нужные настройки из файла .env
    Если какой-то переменной в файле не будет,
    То сразу выйдет ошибка в config.py
    '''
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    debug: bool = False
    model_config = {
        # имя файла с переменными окружения
        "env_file": ".env",
        # кодировка этого файла
        "env_file_encoding": "utf-8",
    }
settings = Settings()