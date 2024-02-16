import datetime
import enum
from typing import Annotated, Optional

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, str_256

# ORM
"""
Объект для хранения всех таблиц, которые мы создаём на стороне приложения в декларативном стиле на языке Python
Base.metadata
"""

# Кастомный тип (Integer Primary Key)
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now() + interval '1 day')"),
        onupdate=datetime.datetime.utcnow
    )]


# Определение модели через класс в декларативном стиле
class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str]
    """
    Параметр backref неявно указывает на другой relationship.
    
    В отличии от back_populates, backref автоматически создаст работника (relationship) в модели ResumesOrm.
    
    Это уже устаревший параметр, по этому нужно указывать связи явно через параметр back_populates в обоих моделях 
    """
    resumes: Mapped[list["ResumesOrm"]] = relationship(
        # backref="worker",
        back_populates="worker"
    )

    """
    Параметр primaryjoin используется, если нам нужно загрузить резюме не для всех работников, а для первых 10-ти.
    
    Значение параметра primaryjoin по умолчанию - WorkersOrm.id == ResumesOrm.worker_id (создаётся
    автоматически SQLAlchemy, потому что ResumesOrm.worker_id это внешний ключ - ForeignKey).
    
    Параметр order_by можно использовать для сортировки.
    
    Параметр lazy можно использовать, чтобы указать тип подгрузки по умолчанию. Например, joined, selectin, select 
    (ленивая подгрузка), raze_on_sql. Лучше указывать тип подгрузки явно в самом запросе
    """
    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        # Подгружаются резюме только с рабочей нагрузкой parttime
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')",
        order_by="ResumesOrm.id.desc()",
        # lazy="selectin"
    )


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str_256]
    """
    Есть 3 варианта обозначить необязательный параметр:
    - compensation: Mapped[int] = mapped_column(nullable=True)
    - compensation: Mapped[int | None]
    - compensation: Mapped[Optional[int]]
    """
    compensation: Mapped[str]
    # Параметр является enum (parttime или fulltime)
    workload: Mapped[Workload]
    """
    Есть 2 варианта обозначить параметр с внешним ключом:
    - ForeignKey("workers.id")
    - ForeignKey(WorkersOrm.id) - используется редко, потому что модели обычно разнесены по разным файлам
    
    Также полезно указывать параметр ondelete со значением "CASCADE" (каскадное удаление) или "SET NULL" (обнуление
    параметра) - в этом случае в аннотации Mapped указывается, что значение может быть None. Например, пользователь
    удалил аккаунт и часто нужно, чтобы все записи, которые ассоциируются с этим пользователем удалились.
    
    Каскадное (CASCADE) удаление работает только когда мы удаляем работника из таблицы Workers, если же мы удаляем
    резюме, то все резюме остаются и работник тоже
    """
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    """
    Параметр server_default обозначает какое значение на уровне базы данных должно задаться столбцу по умолчанию.
    В него можно передать, например, "func.now()" (получение местного времени через функцию SQL now). Чтобы указать
    нужный часовой пояс нужно ввести свой SQL запрос, который будет выполнятся для заполнения данного столбца. Например,
    text("TIMEZONE('utc', now())") - (получает текущее время по часовому поясу UTC).
    
    Параметр default позволяет записывать данные в столбец по умолчанию на уровне Python приложения. Например, передать
    в него "datetime.datetime.utcnow()" и тогда со стороны приложения дата и время будут отправляться в базу данных
    """
    created_at: Mapped[created_at]
    """
    Параметр onupdate записывает данные в столбец при обновлении данных (UPDATE). При обновлении резюме запишется
    дата и время обновления данных в столбец updated_at.
    
    Если мы будем делать прямые запросы (без ORM), то этот аргумент не всегда будет подставляться. По этому имеет смысл
    на уровне базы данных реализовать обновление столбца. Например, в Postgres это можно сделать через триггеры,
    триггерную функцию можно пережать в параметр - server_onupdate
    
    Создание триггерных в PostgreSQL
        CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
       NEW.updated_at = TIMEZONE('utc', CURRENT_TIMESTAMP); -- или просто CURRENT_TIMESTAMP, если не нужна таймзона UTC
       RETURN NEW;
    END;
    $$ language 'plpgsql';
    
    CREATE OR REPLACE TRIGGER updated_at_workers BEFORE INSERT OR UPDATE
        ON workers FOR EACH ROW EXECUTE PROCEDURE
        update_updated_at_column();
    
    CREATE OR REPLACE TRIGGER updated_at_resumes BEFORE INSERT OR UPDATE
        ON resumes FOR EACH ROW EXECUTE PROCEDURE
        update_updated_at_column();
    """
    updated_at: Mapped[updated_at]

    """
    Параметр back_populates - название relationship с которым делается связь (убирает ошибку - SAWarning).
    
    Например, мы задаём работника
    workers = WorkersOrm(name="Artem")
    
    Добавляем работнику какое-то резюме
    workers.resumes.append(ResumesOrm)
    
    Суть в том, что когда мы захотим обратиться к резюме из списка, то у этого резюме будет параметр worker, который
    будет ссылаться на созданного работника - Artem. Для этого нужен back_populates и также он нужен, чтобы не было
    ошибок SAWarning в консоли
    workers.resumes[0].worker
    """
    worker: Mapped["WorkersOrm"] = relationship(
        back_populates="resumes",
    )

    vacancies_replied: Mapped[list["VacanciesOrm"]] = relationship(
        back_populates="resumes_replied",
        secondary="vacancies_replies",
    )

    repr_cols_num = 2
    repr_cols = ("created_at", )

    # Различные параметры таблицы
    __table_args__ = (
        # Первичные ключи таблицы (можно задавать тут, например, для связи Many To Many)
        # PrimaryKeyConstraint("id", "title")
        # Индексация работников по названию резюме (синтаксис: название индекса, название столбцов для индекса)
        Index("title_index", "title"),
        # Constraint (ограничение) - например, мы хотим, чтобы compensation всегда были > 0 (для согласованности данных)
        CheckConstraint("compensation > 0", "check_compensation_positive")
    )

    # Метод используется для красивого вывода модели в логе (если моделей много, то лучше определить общий repr)
    # def __repr__(self):
    #     return f"<Resume id={self.id}, ...все столбцы таблицы resumes...>"


class VacanciesOrm(Base):
    """
    В параметре secondary указывается название таблицы через которую связано relationship с моделью resumes.
    Таблица vacancies связана с resumes через вторую таблицу vacancies_replies (вторая таблица)
    """
    __tablename__ = "vacancies"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]

    resumes_replied: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="vacancies_replied",
        secondary="vacancies_replies",
    )


class VacanciesRepliesOrm(Base):
    """
    Связующая таблица (вторая таблица) с откликами со связью Many To Many
    """
    __tablename__ = "vacancies_replies"

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # Дополнительный столбец (сопроводительное письмо)
    cover_letter: Mapped[Optional[str]]


# Императивный стиль определения таблыц
# Объект для хранения всех таблиц, которые мы создаём на стороне приложения в императивном стиле на языке Python
metadata_obj = MetaData()

# Определение модели через класс Table в императивном стиле
workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

resumes_table = Table(
    "resumes",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String(256)),
    Column("compensation", Integer, nullable=True),
    Column("workload", Enum(Workload)),
    Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column("updated_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow),
)
