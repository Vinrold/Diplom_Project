from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.dependencies import get_db
from app.models.comics import Comics
from app.schemas.comics import ComicsCreate, ComicsResponse, ComicsUpdate

router = APIRouter(
    # начало эндпоинтов - префикс
    prefix="/comics",
    tags=["comics"],
)


# получение всех Комиксов
@router.get("/", response_model=list[ComicsResponse])
def get_comics(db: Session = Depends(get_db)):
    comics = db.query(Comics).all()
    return comics

# получение комикса по id
@router.get("/{comic_id}", response_model=ComicsResponse)
def get_comic(comic_id: int, db: Session = Depends(get_db)):
    comic = db.query(Comics).filter(Comics.id == comic_id).first()
    if not comic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комикс не найден")
    return comic


# создание комикса
@router.post("/", response_model=ComicsResponse, status_code=status.HTTP_201_CREATED)
def create_comic(comics_data: ComicsCreate, db: Session = Depends(get_db)):

    # 1. сначала нужно проверить, нет ли уже комикса с таким же названием
    existing_by_name = db.query(Comics).filter(Comics.name == comics_data.name).first()
    if existing_by_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Название уже занят")
    
    # если такого названия не было, создаем через ORM
    new_comic = Comics(
        name=comics_data.name,
        description=comics_data.description
    )

    db.add(new_comic) # передали инструкцию БД
    try:
        db.commit() # БД выполнила инструкцию и создала id
        db.refresh(new_comic) # БД записала id в объект
        return new_comic # вернули объект с id, названием и описанием
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать комикс"
        )

# Измение данных комикса
@router.put("/{comic_id}", response_model=ComicsResponse)
def comics_update(comic_id: int, update_data: ComicsUpdate, db: Session = Depends(get_db)):
    # ищем комикс по ид
    comic = db.query(Comics).filter(Comics.id == comic_id).first()
    if not comic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комикс не найден")
    
    # Обновляем те поля что пришли от запроса только те что не None
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(comic, key, value)
    try:
        db.commit()
        db.refresh(comic)
        return comic
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось обновить комикс"
        )


    
    
# удаление комикса
@router.delete("/{comic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comic(comic_id: int, db: Session = Depends(get_db)):
    # чтобы удадить комикс по id, нужно сначала найти его
    comic = db.query(Comics).filter(Comics.id == comic_id).first()
    if not comic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комикс не найден")
    db.delete(comic) #просим БД удалить строку из таблицы с этим комиксом
    try:
        db.commit() #БД удаляет строку
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неудалось удалить комикс"
        )