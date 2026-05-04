"""Task model helpers."""

from models.database import query_db, execute_db


def create_task(poster_id, title, description, category, budget,
                lat, lng, radius_km=5, suggested_min=None,
                suggested_max=None, photo_path=None):
    """Insert a new task and return its id."""
    task_id = execute_db(
        """INSERT INTO tasks
           (poster_id, title, description, category, budget,
            lat, lng, radius_km, suggested_price_min, suggested_price_max, photo_path)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (poster_id, title, description, category, budget,
         lat, lng, radius_km, suggested_min, suggested_max, photo_path)
    )
    return task_id


def get_task_by_id(task_id):
    """Get a single task by id."""
    return query_db("SELECT * FROM tasks WHERE id = ?", (task_id,), one=True)


def get_all_tasks():
    """Return all tasks ordered by newest first."""
    return query_db("SELECT * FROM tasks ORDER BY created_at DESC")


def get_tasks_by_poster(poster_id):
    """Return all tasks by a specific poster."""
    return query_db(
        "SELECT * FROM tasks WHERE poster_id = ? ORDER BY created_at DESC",
        (poster_id,)
    )


def update_task_status(task_id, status):
    """Update the status of a task."""
    execute_db("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))


def update_task_category(task_id, category, suggested_min=None, suggested_max=None):
    """Update AI-detected category and suggested price for a task."""
    execute_db(
        """UPDATE tasks SET category = ?, suggested_price_min = ?,
           suggested_price_max = ? WHERE id = ?""",
        (category, suggested_min, suggested_max, task_id)
    )
