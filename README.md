# Task Management API

A FastAPI-based task management application with a simple HTML frontend and SQLite database persistence.

The app supports creating, listing, updating, and deleting tasks, plus filtering by status and priority and searching by title or description. Data is stored in `task.db` using SQLAlchemy.

## Features

- FastAPI REST API for task CRUD operations
- SQLite database with SQLAlchemy ORM
- Jinja2-rendered frontend at `/`
- Filter tasks by `status` and `priority`
- Search tasks by title or description
- Pydantic request/response validation
- Automatic table creation on app startup
- Pytest coverage for core API behavior

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Jinja2
- pytest
- uv / `pyproject.toml`

## Project Structure

```text
.
├── app/
│   ├── database/
│   │   └── todo_database.py      # SQLAlchemy engine, session, base, DB dependency
│   ├── models/
│   │   └── task_models.py        # SQLAlchemy Task model
│   ├── routes/
│   │   └── tasks.py              # API routes and frontend route
│   ├── schemas/
│   │   └── task_shemas.py        # Pydantic schemas for create/update/response
│   ├── services/
│   │   └── task_services.py      # Database CRUD and filtering logic
│   ├── templates/
│   │   └── index.html            # HTML frontend
│   └── main.py                   # FastAPI app entrypoint
├── static/                       # Static files mounted at /static
├── tests/
│   └── test_tasks.py             # API tests
├── seed.py                       # Optional script to insert sample tasks
├── task.db                       # SQLite database file
├── pyproject.toml                # Project dependencies and pytest config
├── uv.lock                       # Lockfile
└── README.md
```

## Setup

1. Install [uv](https://astral.sh/uv/) if you do not already have it.
2. Install dependencies:

```bash
uv sync
```

3. Start the development server:

```bash
uv run uvicorn app.main:app --reload --port 8000
```

4. Open the app in your browser:

- Frontend: `http://localhost:8000/`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database

- The app uses SQLite with database file `task.db`
- Tables are created automatically on startup with:

```python
BASE.metadata.create_all(bind=engine)
```

- Database connection setup lives in `app/database/todo_database.py`

## Seed Sample Data

To insert a couple of example tasks into the database:

```bash
uv run python seed.py
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Render the HTML frontend |
| `POST` | `/tasks` | Create a new task |
| `GET` | `/tasks` | List tasks with optional filters |
| `GET` | `/tasks/{task_id}` | Get one task by ID |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

## Query Parameters

`GET /tasks` supports:

- `status`: `todo`, `in_progress`, `done`
- `priority`: `low`, `medium`, `high`
- `search`: substring match against title or description

Example:

```text
/tasks?status=todo&priority=high&search=homework
```

## Task Fields

### Create task

```json
{
  "title": "Finish homework",
  "description": "Math exercises for tomorrow",
  "status": "todo",
  "priority": "high",
  "tags": ["school"]
}
```

### Response task

```json
{
  "id": 1,
  "title": "Finish homework",
  "description": "Math exercises for tomorrow",
  "status": "todo",
  "priority": "high",
  "tags": ["school"],
  "created_at": "2026-05-29T10:00:00Z",
  "updated_at": "2026-05-29T10:00:00Z"
}
```

## Testing

Run the test suite with:

```bash
uv run pytest
```

The current tests cover:

- task creation
- listing tasks
- validation errors
- fetching a task by ID
- 404 handling for missing tasks

## Notes

- Task tags are stored in the database as a comma-separated string and converted back to a list in the service layer
- The frontend currently supports creating, listing, filtering, searching, and deleting tasks
- The project uses SQLite locally, so it is easy to run without extra setup
