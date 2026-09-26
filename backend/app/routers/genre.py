from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_db
from app.models.genres import Genres
from app.schemas.genres import GenreCreate, GenreResponse, GenreUpdate

router = APIRouter(
    prefix="/genre",
    tags=["genre"],
)


# Весь список жанров
@router.get("/", response_model=list[GenreResponse])
def get_genres(db: Session = Depends(get_db)):
    genres = db.query(Genres).all()
    return genres


# Добавление Жанра
@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
def create_genre(genre_data: GenreCreate, db: Session = Depends(get_db)):
    
    # проверка есть ли такой жанр в списке
    existing_name = db.query(Genres).filter(Genres.name == genre_data.name).first()
    if existing_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Название уже занято")

    # создаем 
    new_genre = Genres(name=genre_data.name)
    # добавляем
    db.add(new_genre)
    try:
        db.commit()
        db.refresh(new_genre)
        return new_genre
    # если что то пошло не так и жанр не записался
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Неудалось добавить жанр")


# Изменение жанра
@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(genre_id: int, update_data:GenreUpdate, db: Session = Depends(get_db)):

    # Поиск жанра по ID
    genre = db.query(Genres).filter(Genres.id == genre_id).first()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Жанр не найдено"
        )

    # принахождении обновляем
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(genre, key, value)
    try:
        db.commit()
        db.refresh(genre)
        return genre
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="неудалось обновить запись про жанр"
        )


# удаление жанра
@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genres).filter(Genres.id == genre_id).first()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Жанр не найден"
        )
    # Удаление
    db.delete(genre)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить Жанр"
        )
    
