from app.database import SessionLocal
from app.models.tags import Tags

TAGS = [
    # Аудитория и возраст
    "для подростков",
    "18+",
    "семейное чтение",
    
    # Формат и структура
    "сингл",
    "мини-серия",
    "онгоинг",
    "ваншот",
    
    # Стиль и подача
    "цветная",
    "чёрно-белая",
    "вебтун",
    "манга-стиль",
    
    # Настроение и тон
    "мрачное",
    "лёгкое",
    "ироничное",
    
    # Происхождение
    "русская",
    "зарубежная",
    "инди",
]

def seed_tags():
    db = SessionLocal()
    try:
        added = 0
        for name in TAGS:
            exists = db.query(Tags).filter(Tags.name == name).first()
            if exists:
                continue
            db.add(Tags(name=name))
            added += 1
        db.commit()
        print(f"Готово! Добавлено тэгов: {added}, всего в базе: {db.query(Tags).count()}")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при заполнении тэгов: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_tags()