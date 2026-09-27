from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_db
from app.models.tags import Tags
from app.schemas.tags import TagCreate, TagResponse, TagUpdate

router = APIRouter(
    prefix="/tag",
    tags=["tag"],
)


# Весь список Тэгов
@router.get("/", response_model=list[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tags).all()
    return tags


# Добавление Тэга
@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(tag_data: TagCreate, db: Session = Depends(get_db)):
    
    # проверка есть ли такой Тэг в списке
    existing_name = db.query(Tags).filter(Tags.name == tag_data.name).first()
    if existing_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Название уже занято")

    # создаем 
    new_tag = Tags(name=tag_data.name)
    # добавляем
    db.add(new_tag)
    try:
        db.commit()
        db.refresh(new_tag)
        return new_tag
    # если что то пошло не так и тэг не записался
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Неудалось добавить Тэг")


# Изменение Тэга
@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, update_data:TagUpdate, db: Session = Depends(get_db)):

    # Поиск Тэга по ID
    tag = db.query(Tags).filter(Tags.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тэга не найдено"
        )

    # принахождении обновляем
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(tag, key, value)
    try:
        db.commit()
        db.refresh(tag)
        return tag
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="неудалось обновить запись про Тэг"
        )


# удаление тэг
@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tags).filter(Tags.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тэг не найден"
        )
    # Удаление
    db.delete(tag)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить Тэг"
        )
    
