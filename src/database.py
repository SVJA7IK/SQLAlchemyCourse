from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import URL, create_engine, text, String
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings


# Создание синхронного движка для работы с базой данных
sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,  # Количество соединений с базой данных
    max_overflow=10,  # Дополнительное количество соединений с базой данных (того, допустимо максимум 15 соединений)
)

# Создание асинхронного движка для работы с базой данных
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

# Создание синхронной фабрики сессий
session_factory = sessionmaker(sync_engine)
# Создание асинхронной фабрики сессий
async_session_factory = async_sessionmaker(async_engine)


str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    # Количество колонок для вывода (начиная с 1 колонки)
    repr_cols_num = 3

    # Список колонок, которые нужно вывести дополнительно
    repr_cols = tuple()

    def __repr__(self):
        """
        Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам в синхронном варианте.
        В асинхронным варианте обращение к relationships выдаст ошибку
        """
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
