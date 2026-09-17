from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import app.models
from app.database import engine, Base
from app.routers import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске сервера он будет переводить модели ORM в таблицы БД
    Base.metadata.create_all(bind=engine)
    yield

# объект, который управляет бэкендом в целом
app = FastAPI(
    lifespan=lifespan,
    title="Проект",
    description="FastAPI+React+PostgreSQL",
    version="1.0.0",
)
# настройка CORS, чтобы сервер не банил наш же сайт
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #по факту ip и порт от клиента
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

@app.get("/")
def root():
    return {
        "message": "Сервер запущен"
    }