# Лабораторна робота №2 — Expenses REST API (Flask)

## Мета роботи
Розробити REST API застосунок для обліку витрат із використанням Flask.  
Реалізувати CRUD-операції для сутностей: User, Category, Record.  
Протестувати API через Postman (колекція та середовища).

---

## Використані технології
- Python 3.11  
- Flask  
- Gunicorn  
- Docker / Render  
- Postman  

---

## Структура проєкту
lab2-expenses-api/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── render.yaml
├── Procfile
├── postman/
│ ├── ExpenseTracker.postman_collection.json
│ ├── env/
│ │ ├── local.postman_environment.json
│ │ └── prod.postman_environment.json
│ └── flows/
│ └── flow.png
└── README.md

---

## Деплой на Render

### Production URL
Healthcheck: https://<твій_сервіс>.onrender.com/healthcheck  
Base URL: https://<твій_сервіс>.onrender.com

### Build / Start
Build Command: `pip install -r requirements.txt`  
Start Command: `gunicorn -b 0.0.0.0:$PORT app:app`  
Region: Frankfurt  
Plan: Free

---

## Приклади запитів (Postman)

| Метод | Endpoint | Опис |
|-------|-----------|------|
| GET | `/healthcheck` | Перевірка працездатності |
| POST | `/user` | Створення користувача |
| GET | `/users` | Отримати список користувачів |
| POST | `/category` | Створення категорії |
| GET | `/category` | Отримати всі категорії |
| POST | `/record` | Створення запису витрат |
| GET | `/record?user_id=1` | Отримати записи користувача |
| DELETE | `/record/1` | Видалити запис за id |

---

## Тестування у Postman
1. Імпортувати колекцію `ExpenseTracker.postman_collection.json`
2. Імпортувати середовища:
   - `env/local.postman_environment.json`
   - `env/prod.postman_environment.json`
3. Виконати запити у порядку:
   - Healthcheck  
   - Create user  
   - Create category  
   - Create record  
   - List records  
   - Delete record  

---

## Експорт для здачі
- Колекція Postman (.json)
- Environment (Local і Production)
- Посилання:
  - GitHub репозиторій: https://github.com/FA1RY2412/lab2-expenses-api
  - Render Deployment: [lab2-expenses-api.onrender.com](https://lab2-expenses-api.onrender.com/)
  - Healthcheck: [lab2-expenses-api.onrender.com/healthcheck](https://lab2-expenses-api.onrender.com/healthcheck)
  - Users: [lab2-expenses-api.onrender.com/healthcheck](https://lab2-expenses-api.onrender.com/users)
  - Category [https://lab2-expenses-api.onrender.com/category](https://lab2-expenses-api.onrender.com/category)
---
