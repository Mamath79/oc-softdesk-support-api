# SoftDesk Support API

&#x20;  &#x20;

> **Educational project (OpenClassrooms)** — backend REST API for managing software projects, issues and comments with role‑based permissions and JWT authentication.

---

## ✨ Features

- 🔐 **JWT authentication** (access/refresh)
- 👥 **Role‑based authorization** per project (owner, contributor)
- 📦 **Projects** with members
- 🐞 **Issues** (title, description, tag, priority, status, assignee)
- 💬 **Comments** on issues
- 🧹 Clean, layered Django + DRF structure

---

## 🧱 Tech stack

- **Python 3.11+**
- **Django 4.x**, **Django REST Framework 3.x**
- **djangorestframework-simplejwt** for tokens
- **SQLite** (dev) — easily swappable to Postgres/MySQL

---

## 🗂️ Project structure (excerpt)

```
softdesk/
├─ manage.py
├─ softdesk/                  # settings / urls / wsgi
├─ api/                       # domain app
│  ├─ models.py               # Project, Issue, Comment, Membership
│  ├─ serializers.py
│  ├─ permissions.py
│  ├─ views.py
│  ├─ urls.py                 # /api/...
│  └─ tests/                  # optional tests folder
└─ requirements.txt
```

---

## 🏁 Quickstart

### 1) Clone & create a virtualenv

```bash
git clone https://github.com/Mamath79/oc-softdesk-support-api.git
cd oc-softdesk-support-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Environment variables

Create a `.env` file at the project root:

```
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
ALLOWED_HOSTS=*
# JWT defaults are fine, but you can tune lifetime if needed
```

### 3) Migrate & run

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Server runs on: `http://127.0.0.1:8000/`

---

## 🔑 Authentication

### Obtain tokens

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass1234"}'
```

**Response**

```json
{
  "access": "<ACCESS_TOKEN>",
  "refresh": "<REFRESH_TOKEN>"
}
```

Use the access token in `Authorization: Bearer <token>`.

---

## 📚 REST endpoints (summary)

> Prefix: `/api/`

### Auth

- `POST /auth/signup/` – create account
- `POST /auth/login/` – obtain JWT tokens
- `POST /auth/refresh/` – refresh access token

### Projects

- `GET /projects/` – list projects (you own or you’re a member of)
- `POST /projects/` – create a project (owner = requester)
- `GET /projects/{id}/` – retrieve
- `PATCH /projects/{id}/` – update (owner only)
- `DELETE /projects/{id}/` – delete (owner only)
- `POST /projects/{id}/members/` – add contributor (owner only)
- `DELETE /projects/{id}/members/{user_id}/` – remove contributor (owner only)

### Issues

- `GET /projects/{id}/issues/` – list project issues
- `POST /projects/{id}/issues/` – create issue (project members)
- `GET /projects/{id}/issues/{issue_id}/` – retrieve
- `PATCH /projects/{id}/issues/{issue_id}/` – update (author or owner)
- `DELETE /projects/{id}/issues/{issue_id}/` – delete (author or owner)

### Comments

- `GET /projects/{id}/issues/{issue_id}/comments/`
- `POST /projects/{id}/issues/{issue_id}/comments/`
- `GET /projects/{id}/issues/{issue_id}/comments/{comment_id}/`
- `PATCH /projects/{id}/issues/{issue_id}/comments/{comment_id}/` (author)
- `DELETE /projects/{id}/issues/{issue_id}/comments/{comment_id}/` (author or owner)

---

## 🧪 Example requests

### Create a project

```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign",
    "description": "Marketing site overhaul"
  }'
```

### Add a contributor

```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/members/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 5}'
```

### Create an issue

```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/issues/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cannot log in",
    "description": "JWT expired issue",
    "tag": "BUG",            # BUG | FEATURE | TASK
    "priority": "HIGH",      # LOW | MEDIUM | HIGH
    "status": "OPEN",        # OPEN | IN_PROGRESS | CLOSED
    "assignee": 5
  }'
```

### Comment an issue

```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/issues/3/comments/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"content":"We’re investigating"}'
```

---

## 🔒 Authorization model

- **Project Owner**: full control on their projects (CRUD, manage members, moderate issues/comments)
- **Contributor**: can create issues & comments, edit their own items, view project
- **Non‑member**: no access

Custom DRF permissions enforce these rules at view/serializer level.

---

## 🛠️ Development notes

- Formatting/linting (optional): `black`, `ruff`
- Consider adding **OpenAPI** with `drf-spectacular` → `/schema/` & Swagger UI
- Postman collection (optional): export to `docs/SoftDesk.postman_collection.json`
- Switch to **PostgreSQL** by adjusting `DATABASES` in settings + env vars

---

## 🧪 Tests (optional)

If you add tests:

```bash
pytest -q
```

---

## 🚀 Deployment

- Configure a production DB (Postgres)
- Set `DJANGO_DEBUG=False`, proper `ALLOWED_HOSTS`
- Collect static files if you add admin or static assets:

```bash
python manage.py collectstatic --noinput
```

- Run via WSGI (gunicorn/uvicorn + reverse proxy) or containerize with Docker

---

## 📜 License

This repository is published for **educational purposes** (OpenClassrooms). If you intend to reuse/redistribute, add a license file (e.g., MIT) and update this section.

---

## 👤 Author

**Mathieu Vieillefont**\
🔗 LinkedIn: [https://www.linkedin.com/in/mathieu-vieillefont/](https://www.linkedin.com/in/mathieu-vieillefont/)\
📧 Email: [mathieu.vieillefont@gmail.com](mailto\:mathieu.vieillefont@gmail.com)

