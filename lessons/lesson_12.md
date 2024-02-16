### SQLAlchemy: Many-to-many relationship (m2m)

Конспект по видео - [ссылка](https://www.youtube.com/watch?v=iPyTC5T9rxg&list=PLeLN0qH0-mCXARD_K-USF2wHctxzEVp40&index=12)

Например, любая вакансия может иметь множество откликов от разных резюме - это называется Many To Many связь.

В таблице со связью **Many To Many** первичный ключ - это отдельная колонка или объединение двух внешних ключей. Могут быть дополнительные столбцы по желанию (пример дополнительного столбца - `VacanciesRepliesOrm.cover_letter`)
