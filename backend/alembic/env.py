from dotenv import load_dotenv
load_dotenv()

import os
from logging.config import fileConfig


from sqlalchemy import engine_from_config, pool
from alembic import context

# Импортируем Base и все модели
from app.database import Base
from app.models.comics import Comics
from app.models.user import User
from app.models.tags import Tags
from app.models.genres import Genres
from app.models.chapters import Chapters
from app.models.pages import Pages
from app.models.comments import Comments
from app.models.favourites import Favourites
from app.models.genres_comics import Genres_comicses
from app.models.tag_comics import Tag_comics

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Берём URL из .env
url = os.getenv("DATABASE_URL")
if not url:
    raise RuntimeError(
        "Переменная окружения DATABASE_URL не найдена! "
        "Проверь .env и перезапусти терминал/VS Code."
    )
config.set_main_option("sqlalchemy.url", url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
