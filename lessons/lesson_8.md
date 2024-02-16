### SQLAlchemy: How to JOIN tables | CTE | Subqueries | Window functions #8

Конспект по видео - [ссылка](https://www.youtube.com/watch?v=203RAaYW83A&list=PLeLN0qH0-mCXARD_K-USF2wHctxzEVp40&index=8)

Функция JOIN в SQLAlchemy делается через метод .join. Есть несколько типов join.

* По умолчанию INNER JOIN - дополнительные аргументы не нужны 
* Если мы хотим сделать FULL JOIN - указывается аргумент full=True
* Если мы хотим сделать LEFT JOIN - указывается аргумент isouter=True

В SQLAlchemy нет RIGHT JOIN, потому что всегда правый можно сделать левым.

Если под-запросу или CTR не указывать название, то он будет автоматически назван - anon...

В методе .select() SQLAlchemy нельзя указать явно все столбцы через "*", для этого нужно указать явно каждый столбец.

Метод .decs() сортирует значения по убыванию, а .ask() по возрастанию (по не убыванию)

