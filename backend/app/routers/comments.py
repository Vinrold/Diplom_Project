from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_db
from app.models.comments import Comments
from app.models.comics import Comics
from app.schemas.comments import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


# Весь список коментариев в определенном комиксе
@router.get("/", response_model=list[CommentResponse])
def get_comments(commics_id: Optional[int] = None, db: Session = Depends(get_db)):

    # все комменты
    query = db.query(Comments)

    # поиск комикса по ID
    if commics_id is not None:
        comic = db.query(Comics).filter(Comics.id == commics_id).first()
        if not comic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комикс не найден")

        # остеивание коментов по ID  комикса
        query = query.filter(Comments.comics_id == commics_id)
    
    comments = query.all()
    return comments


# Добавление коментария пользователем
@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(comment_data: CommentCreate, db:Session = Depends(get_db)):
    user_id = comment_data.user_id

    # есть ли коммикс
    comic = db.query(Comics).filter(Comics.id == comment_data.comics_id).first()
    if not comic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комикс не найден")

    # данные для создания  коментария
    new_commet = Comments(
        user_id=user_id,
        comics_id=comment_data.comics_id,
        content=comment_data.content
    )

    # добавляем новую запись в базу
    db.add(new_commet)
    try:
        db.commit()
        db.refresh(new_commet)
        return new_commet
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось добавить коментарий  "
        )

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id:int, update_data:CommentUpdate, db: Session = Depends(get_db)):
    

