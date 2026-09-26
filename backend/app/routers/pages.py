from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_db
from app.models.pages import Pages
from app.schemas.pages import PageCreate, PageResponse, PageUpdate

router = APIRouter(
    prefix="/pages",
    tags=["pages"],
)

# показать изображения которые принадлежать выбранному комиксу ивыбраной главе
@router.get("/", response_model=list[PageResponse])
def get_pages(
    comics_id: Optional[int] = None,
    chapters_id: Optional[int] = None,
    db: Session = Depends(get_db)):
    
    # Получение страниц 
    query = db.query(Pages)
    # Все страницы по комиксу
    if comics_id is not None:
        query = query.filter(Pages.comics_id == comics_id)
    # Все страницы конкретной главы
    if chapters_id is not None:
        query = query.filter(Pages.chapters_id == chapters_id)
    #  если глав нет
    pages = query.all()
    if not pages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Изображение не найдено"
            )
    return pages

@router.post("/", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
def created_page(page_data: PageCreate, db:Session = Depends(get_db)):
    #  Проверка уникальности: comics_id + chapters_id +number
    existing = db.query(Pages).filter(
        Pages.comics_id == page_data.comics_id,
        Pages.chapters_id == page_data.chapters_id,
        Pages.number == page_data.number
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Страница с таким номером уже есть в этой главе"
        )

    # Новое изображение
    new_page = Pages(
        number=page_data.number,
        comics_id=page_data.comics_id,
        chapters_id=page_data.chapters_id,
        image_url=page_data.image_url
    )

    # Добавление новой записи о изображении
    db.add(new_page)
    try:
        db.commit()
        db.refresh(new_page)
        return new_page
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неудалось добавить изображение"
        )

# Обновление изображения
@router.put("/{page_id}", response_model=PageResponse)
def update_page(
    page_id: int,
    update_data: PageUpdate,
    db: Session = Depends(get_db)    
):
    # поиск зображения по ИД
    page = db.query(Pages).filter(Pages.id == page_id).first()
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="изображение не найдено"
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(page, key, value)

    try:
        db.commit()
        db.refresh(page)
        return page
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="неудалось обновить запись про изображение"
        )
    
@router.delete("/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_page(
    page_id: int,
    db: Session = Depends(get_db)
):
    # поиск изображения по ИД
    page = db.query(Pages).filter(Pages.id == page_id).first()
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Изображение не найдено"
        )
    db.delete(page)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить страницу"
        )

    
    
    
    