# Task Management API

A simple, fast FastAPI-based task management application with CRUD operations, filtering, search, and HTML frontend.

Uses in-memory storage (no database), Pydantic validation, Jinja2 templating, and pytest for tests. Managed with uv/pyproject.toml.

## Features

- Create, read, update, delete tasks (CRUD)
- Filter tasks by status (`todo`, `in_progress`, `done`), priority (`low`, `medium`, `high`), tags (exact list match)
- Search tasks by substring in title/description (case-insensitive)
- Automatic ID and timestamp generation
- Input validation with Pydantic (Literal enums for status/priority)
- HTML frontend at `/` (index.html)
- API documentation auto-generated at `/docs` (Swagger) or `/redoc`
- Comprehensive unit tests

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI app setup and routers
│   ├── models.py            # Pydantic Task/TaskCreate models
│   ├── routes/
│   │   └── tasks.py         # API endpoints (CRUD, filter)
│   ├── services/
│   │   └── task_services.py # Business logic (in-memory CRUD/filter)
│   └── templates/
│       └── index.html       # Frontend HTML template
├── static/                  # CSS/JS/assets (mounted at /static)
├── tests/
│   └── test_tasks.py        # Pytest API tests
├── pyproject.toml           # Dependencies (uv/FastAPI/Pydantic/etc.)
├── uv.lock                  # Lockfile
├── README.md                # This file
└── TODO.md                  # Task progress tracker (added by BLACKBOXAI)
```

## Setup & Installation

1. Ensure [uv](https://astral.sh/uv) is installed (`pipx install uv` or brew).
2. Install dependencies:
   ```
   uv sync
   ```
3. Run the development server:
   ```
   uvicorn app.main:app --reload --port 8000
   ```
4. Open http://localhost:8000 in browser.
   - Frontend: http://localhost:8000/
   - API Docs: http://localhost:8000/docs
   - Redoc: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint     | Description                  | Params/Query                  | Response          |
|--------|--------------|------------------------------|-------------------------------|-------------------|
| GET    | `/`          | Render HTML frontend        | -                             | HTML page         |
| POST   | `/tasks`     | Create task                 | Body: TaskCreate              | 201 Task          |
| GET    | `/tasks`     | List/filter tasks           | ?status=?&priority=?&tags=?&search=? | 200 [Task] |
| GET    | `/tasks/{id}`| Get task by ID              | path id (int)                 | 200 Task or 404   |
| PUT    | `/tasks/{id}`| Update task                 | path id, Body: TaskCreate     | 200 Task          |
| DELETE | `/tasks/{id}`| Delete task by ID           | path id                       | 200 (no content)  |

**Task Fields:**
- `id`: int (auto)
- `title`: str (req)
- `description`: str (req)
- `status`: "todo" \| "in_progress" \| "done" (default "todo")
- `priority`: "low" \| "medium" \| "high" (default "low")
- `tags`: ["str"] (default [])
- `created_at`: datetime (auto)

## Testing

Run tests:
```
pytest
```
All tests pass (covers create/list/validation/get/404).

## Notes / Improvements

- **In-memory only**: Data lost on restart. Add SQLAlchemy + DB (SQLite/Postgres) for persistence.
- Typos in code (e.g., `creat_task`): Not fixed per task scope (comments only).
- Tags filter: Exact list match; improve to any tag intersection.
- Filtering chain: Sequential (order matters); consider more advanced queries.
- No auth/rate limiting.
- Frontend: Basic index.html; enhance with JS for dynamic CRUD.

## Dependencies

See `pyproject.toml` / `uv.lock`. Key: FastAPI, Pydantic, Jinja2, pytest.


