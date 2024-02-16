### SQLAlchemy results to Pydantic schema using FastAPI #11

Конспект по видео - [ссылка](https://www.youtube.com/watch?v=jiS2CmvPTfM&list=PLeLN0qH0-mCXARD_K-USF2wHctxzEVp40&index=11)

Если в API есть POST запросы, то обычно принято писать модель для POST запроса (например, `WorkersAddDTO`) и потом уже наследуясь от неё делать модель для GET запроса (например, `class WorkersDTO(WorkersAddDTO)`).

Класс для передачи данных (например, модель GET или POST запроса) можно называть **DTO** - Data Transfer Object. Такой класс обычно используется для передачи данных между сервисами приложения
