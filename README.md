# Lab 2 — Basic REST API (Expenses Tracker)

Це простий REST API для обліку витрат **без бази даних** (усі дані зберігаються в пам'яті). Реалізовано повний набір ендпоінтів з методички.

## 🚀 Швидкий старт (локально)

Вимоги: Python 3.11+

```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
python app.py  # сервер на http://localhost:8080
```

Перевірка:
```
GET http://localhost:8080/healthcheck
```

## 🌐 Деплой на Render.com

1. Створи новий репозиторій на GitHub і залий цей проєкт.
2. На Render: **New +** → **Web Service** → **Connect** до твого репозиторію.
3. Runtime: *Python*, Build Command: `pip install -r requirements.txt`, Start Command: `gunicorn app:app`
4. Region: *Frankfurt* (EU), Plan: *Free*.
5. Збережи. Після деплою отримаєш URL виду `https://<your-service>.onrender.com`.

> Альтернатива: деплой через `render.yaml` (Auto Deploy), або Docker.

## 🧪 Postman

У папці `postman/` є:
- **ExpenseTracker.postman_collection.json** — повна колекція запитів
- **env/local.postman_environment.json** — environment для локального запуску
- **env/production.postman_environment.json** — приклад для продакшн-URL
- **flows/flow.md** — інструкції з побудови Postman Flow (5 хвилин)

### Імпорт
1. В Postman: **Import** → імпортуй колекцію та потрібні environment-и.
2. Обери environment (Local або Production).
3. Запусти запити у вказаному порядку (або створіть Flow за інструкцією).

## 📚 Ендпоінти

### Users
- `GET /user/<user_id>` — отримати користувача
- `DELETE /user/<user_id>` — видалити користувача (і його записи)
- `POST /user` — створити користувача (`{{"name":"Alice"}}`)
- `GET /users` — список користувачів

### Categories
- `GET /category` — список категорій
- `POST /category` — створити категорію (`{{"name":"Food"}}`)
- `DELETE /category?id=<id>` або `DELETE /category/<id>` — видалити категорію (і записи в ній)

### Records
- `GET /record/<record_id>` — отримати запис
- `DELETE /record/<record_id>` — видалити запис
- `POST /record` — створити запис (`{{"user_id":1, "category_id":1, "amount":12.5}}`)
- `GET /record?user_id=1&category_id=2` — фільтр за `user_id` і/або `category_id` (мінімум один параметр обов'язковий, інакше 400)

### Health
- `GET /healthcheck` — простий healthcheck

## 🧾 Приклади тіла запитів

**POST /user**
```json
{"name": "Charlie"}
```

**POST /category**
```json
{"name": "Sport"}
```

**POST /record**
```json
{"user_id": 1, "category_id": 1, "amount": 99.99}
```

## ✅ Здача в Classroom
- Посилання на GitHub
- Посилання на Render (прод URL)
- Файл колекції Postman (+ environments)
- Скрин або коротке відео Postman Flow (за бажанням — файл з Flow)

---

© 2025
