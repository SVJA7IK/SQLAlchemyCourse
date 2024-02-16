### SQLAlchemy: Database connection, raw SQL queries with engine #2
Конспект по видео - [ссылка](https://www.youtube.com/watch?v=vh19Mlot0NY&list=PLeLN0qH0-mCXARD_K-USF2wHctxzEVp40&index=2)

DSN - это строка для подключения к базе данных. Например, postgresql+psycopg://postgres:postgres@localhost:5432/sa.
После "+" указывается база данных к которой происходит подключение (указать можно любую).

При создании движка для работы с базой данных желательно включить параметр echo. Это параметр включает отображение
всех запросов в консоли, которые делает SQLAlchemy к базе данных.

Метод движка (engine) - connect() в контекстном менеджере после выполнения запроса автоматически делает ROLLBACK,
а метод begin() автоматически делает COMMIT. Если мы хотим сделать COMMIT, то лучше использовать метод connect(), и
прописать COMMIT явно - conn.commit()