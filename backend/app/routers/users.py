from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    # начало эндпоинтов - префикс
    prefix="/users",
    tags=["users"],
)

# инициализация хешера
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    safe_password = password[:72]
    return pwd_context.hash(safe_password)


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):

    # 1. сначала нужно проверить, нет ли уже пользователя с таким никнеймом
    existing_by_nickname = db.query(User).filter(User.nickname == user_data.nickname).first()
    if existing_by_nickname:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Никнейм уже занят")
    
    # 2. проверка есть ли пользователь с таким email
    existing_by_email  = db.query(User).filter(User.email == user_data.email).first()
    if existing_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже занят")
    
    # если такого логина и эмаила не было, регистрируем через ORM
    # указали инструкцию, ЧТО нужно сделать без id

    # 3. хэшируем пароль перед сохранением
    heshed_password = get_password_hash(user_data.password)


    new_user = User(
        nickname=user_data.nickname,
        email=user_data.email,
        password_hash=heshed_password
    )
    db.add(new_user) # передали инструкцию БД
    try:
        db.commit() # БД выполнила инструкцию и создала id
        db.refresh(new_user) # БД записала id в объект
        return new_user # вернули объект с id, ником и паролем
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось зарегистрировать пользователя"
        )
    

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # чтобы удадить пользователя по id, нужно сначала найти его
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    db.delete(user) #просим БД удалить строку из таблицы с этим пользователем
    try:
        db.commit() #БД удаляет строку
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неудалось удалить пользователя"
        )