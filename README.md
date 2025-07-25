![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

REST API для управления задачами с аутентификацией JWT
## 📌 Возможности
- Создание, чтение, обновление и удаление задач
- Аутентификация по JWT-токенам
- Фильтрация задач по статусу
- Автоматическое проставление даты создания
- Готовность к Docker-развертыванию

Запуск сервера:
bash
uvicorn app.main:app --reload

Переменные окружения (.env):
ini
SECRET_KEY=ваш_секретный_ключ
DATABASE_URL=sqlite:///./task_manager.db
ACCESS_TOKEN_EXPIRE_MINUTES=30

Документация API:
После запуска сервера документация доступна по адресам:
Swagger UI: /docs
ReDoc: /redoc
