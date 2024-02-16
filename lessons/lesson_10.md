### SQLAlchemy: Advanced RELATIONSHIPS | Indexes | Constraints #10

Конспект по видео - [ссылка](https://www.youtube.com/watch?v=WPygSa1kaeM&list=PLeLN0qH0-mCXARD_K-USF2wHctxzEVp40&index=10)

Если нужно подгружать несколько relationships, то это делается через множественный .options().

Типы подгрузки dynamic и subquery являются устаревшими по документации.

Тип подгрузки raze_on_sql вызывает исключение при обращении к атрибуту, до тех пор пока не переопределим в запросе тип подгрузки.

Статья про ограничение подгружаемых связей - https://stackoverflow.com/a/72298903/22259413

Первичные ключи желательно оставлять возле столбцов в модели, а например, Index, Constrain можно указать в параметрах таблицы - `__table_args__`
