from app.database.todo_database import sessionlocal
from app.models.task_models import Task

db = sessionlocal()

tasks = [
    Task(
        title = "sleep",
        description = "I will at 10 pm sleep",
        status = "todo",
        priority = "medium"
    )
    ,
    Task(
        title = "Homework",
        description = "I should do my homework today",
        status = "todo",
        priority = "high"
    )
]


db.add_all(tasks)
db.commit()

print("Done")