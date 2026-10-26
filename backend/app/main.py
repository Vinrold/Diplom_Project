from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from pathlib import Path

import app.models
from app.database import engine, Base
from app.routers import users, auth, chapters, comics, comments, genre, tags, pages

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

# 1. Сначала инициализируем app
app = FastAPI(
    lifespan=lifespan,
    title="Проект",
    description="FastAPI+React+PostgreSQL",
    version="1.0.0",
)

# 2. Рассчитываем BASE_DIR относительно main.py (папка backend)
BASE_DIR = Path(__file__).resolve().parent.parent

# 3. Теперь можно безопасно вызывать mount()
app.mount("/uploads", StaticFiles(directory=BASE_DIR / "uploads"), name="uploads")



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(comics.router)
app.include_router(comments.router)
app.include_router(chapters.router)
app.include_router(pages.router)
app.include_router(genre.router)
app.include_router(tags.router)

@app.get("/")
def root():
    return {"message": "Сервер запущен"}
