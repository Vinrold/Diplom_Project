# app/routers/uploads.py
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.staticfiles import StaticFiles

from app.security import get_current_user
from app.models.user import User

router = APIRouter(tags=["uploads"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # папка создастся, если её нет

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 МБ


@router.post("/uploads")
def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    # проверяем расширение
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Разрешены только изображения: jpg, jpeg, png, webp, gif",
        )

    # генерируем уникальное имя, чтобы два файла с названием «обложка.jpg» не затирали друг друга
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    # читаем содержимое и проверяем размер
    contents = file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл больше 5 МБ",
        )

    with open(file_path, "wb") as f:
        f.write(contents)

    # возвращаем относительный путь — фронтенд склеит его с адресом сервера
    return {"url": f"/uploads/{unique_name}"}
