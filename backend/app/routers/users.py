from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    # начало эндпоинтов - префикс
    prefix="/users",
    tags=["users"],
)

# получение всех пользователь
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# получение пользователя по id
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # сначала нужно проверить, нет ли уже пользователя с таким никнеймом
    exists = db.query(User).filter(User.nickname == user_data.nickname).first()
    if exists:
        raise HTTPException(status_code=400, detail="Никнейм уже занят")
    # если такого логине не было, регистрируем через ORM
    # указали инструкцию, ЧТО нужно сделать без id
    user = User(nickname=user_data.nickname,
                password=user_data.password)
    db.add(user) # передали инструкцию БД
    db.commit() # БД выполнила инструкцию и создала id
    db.refresh(user) # БД записала id в объект
    return user # вернули объект с id, ником и паролем

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # чтобы удадить пользователя по id, нужно сначала найти его
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user) #просим БД удалить строку из таблицы с этим пользователем
    db.commit() #БД удаляет строку