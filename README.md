# Payment API

REST API для управления платежами с авторизацией JWT, ролями пользователей и вебхуками для пополнения баланса.

## Тестовые учетные данные

| Роль | Email | Пароль |
|------|-------|--------|
| Пользователь | `user@example.com` | `user123` |
| Администратор | `admin@example.com` | `admin123` |

> Данные создаются автоматически при миграции.

---

## Запуск с Docker Compose

```bash
git clone https://github.com/Mu1asame7/payment_api.git
cd payment_api
docker compose up --build
```

## Запуск без Docker (локально)

```bash
# 1. Установи PostgreSQL и создай базу данных
psql -U postgres -c "CREATE DATABASE payment_db;"

# 2. Клонируй репозиторий
git clone https://github.com/Mu1asame7/payment_api.git
cd payment_api

# 3. Создай виртуальное окружение
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate          # Windows

# 4. Установи зависимости
pip install -r requirements.txt

# 5. Создай файл .env
echo "DATABASE_URL=postgresql+asyncpg://postgres:ТВОЙ_ПАРОЛЬ@localhost:5432/payment_db" > .env
echo "SECRET_KEY=your-super-secret-key-change-this" >> .env
echo "ALGORITHM=HS256" >> .env
echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env

# 6. Примени миграции
alembic upgrade head

# 7. Запусти сервер
uvicorn app.main:app --reload
