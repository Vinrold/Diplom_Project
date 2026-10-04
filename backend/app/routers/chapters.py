from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_db
from app.models.chapters import Chapters
from app.models.comics import Comics
from app.schemas.chapters import ChapterCreate, ChapterResponse, ChapterUpdate

router = APIRouter(
    prefix="/chapters",
    tags=["chapters"],
)

@router.get("/", response_model=list[ChapterResponse])
def get_chapters(
    comic_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
 
    query = db.query(Chapters)
    if comic_id is not None:
        comic = db.query(Comics).filter(Comics.id == comic_id).first()
        if not comic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комикс не найден")

        query = query.filter(Chapters.comics_id == comic_id)

    chapters = query.all()
    return chapters


@router.get("/{chapter_id}", response_model=ChapterResponse)
def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(Chapters).filter(Chapters.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Глава не найдена"
        )
    return chapter


@router.post("/", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
def create_chapter(
    chapter_data: ChapterCreate,
    db: Session = Depends(get_db)
):
    # Проверка существования комикса (обязательно)
    comic = db.query(Comics).filter(Comics.id == chapter_data.comics_id).first()
    if not comic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Комикс с таким ID не найден"
        )

    # Уникальность номера главы в рамках одного комикса
    existing = db.query(Chapters).filter(
        Chapters.comics_id == chapter_data.comics_id,
        Chapters.number == chapter_data.number
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="В этом комиксе уже есть глава с таким номером"
        )

    new_chapter = Chapters(
        title=chapter_data.title,
        number=chapter_data.number,
        comics_id=chapter_data.comics_id
    )

    db.add(new_chapter)
    try:
        db.commit()
        db.refresh(new_chapter)
        return new_chapter
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать главу"
        )


@router.put("/{chapter_id}", response_model=ChapterResponse)
def update_chapter(
    chapter_id: int,
    update_data: ChapterUpdate,
    db: Session = Depends(get_db),
):
    chapter = db.query(Chapters).filter(Chapters.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Глава не найдена"
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(chapter, key, value)

    try:
        db.commit()
        db.refresh(chapter)
        return chapter
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось обновить главу"
        )


@router.delete("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(Chapters).filter(Chapters.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Глава не найдена"
        )

    db.delete(chapter)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить главу"
        )
