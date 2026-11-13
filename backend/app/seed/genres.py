from app.database import SessionLocal
from app.models.genres import Genres

GENRES = [
    "Супергерои",
    "Фэнтези",
    "Научная фантастика",
    "Хоррор",
    "Детектив",
    "Нуар",
    "Комедия",
    "Драма",
    "Романтика",
    "Приключения",
    "Постапокалипсис",
    "Киберпанк",
    "Сёнэн",
    "Сёдзё",
    "Манхва",
    "Индивидуальная история",
]

def seed_genres():
    db = SessionLocal()
    try:
        added = 0
        for name in GENRES:
            exists = db.query(Genres).filter(Genres.name == name).first()
            if exists:
                continue
            db.add(Genres(name=name))
            added += 1
        db.commit()
        print(f"Готово! Добавлено жанров: {added}, всего в базе: {db.query(Genres).count()}")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при заполнении Жанров: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_genres()