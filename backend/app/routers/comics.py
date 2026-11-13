from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user import User
from app.models.genres import Genres
from app.models.tags import Tags
from app.models.comics import Comics
from app.schemas.comics import ComicsCreate, ComicsResponse, ComicsUpdate
from app.security import get_current_user


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

# Получение публичных комиксов  максимуим 50 шт
@router.get("/public", response_model=list[ComicsResponse])
def get_public_comics(db: Session = Depends(get_db)):
    # Отдаём только опубликованные, максимум 50 штук
    comics = (
        db.query(Comics)
        .filter(Comics.is_published == True)
        .limit(50)
        .all()
    )
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
def create_comic(comics_data: ComicsCreate,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):

    # 1. сначала нужно проверить, нет ли уже комикса с таким же названием
    existing_by_name = db.query(Comics).filter(Comics.name == comics_data.name).first()
    if existing_by_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Название уже занято")
    
    # если такого названия не было, создаем через ORM
    new_comic = Comics(
        name=comics_data.name,
        description=comics_data.description,
        image_url=comics_data.image_url,
        owner_id=current_user.id
    )

    if comics_data.genre_ids:
        new_comic.genres = db.query(Genres).filter(Genres.id.in_(comics_data.genre_ids)).all()


    if comics_data.tag_ids:
        new_comic.tags = db.query(Tags).filter(Tags.id.in_(comics_data.tag_ids)).all()


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
def comics_update(comic_id: int, update_data: ComicsUpdate, current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    # ищем комикс по ид
    comic = db.query(Comics).filter(Comics.id == comic_id).first()
    if not comic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комикс не найден")

    if comic.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на этот комикс")

    
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
def delete_comic(comic_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # чтобы удадить комикс по id, нужно сначала найти его
    comic = db.query(Comics).filter(Comics.id == comic_id).first()
    if not comic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комикс не найден")
    if comic.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на этот комикс")


    db.delete(comic) #просим БД удалить строку из таблицы с этим комиксом
    try:
        db.commit() #БД удаляет строку
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить комикс"
        )