"""Rating model helpers."""

from models.database import query_db, execute_db


def create_rating(rater_id, ratee_id, task_id, score, comment=None):
    """Insert a new rating and return its id."""
    rating_id = execute_db(
        """INSERT INTO ratings (rater_id, ratee_id, task_id, score, comment)
           VALUES (?, ?, ?, ?, ?)""",
        (rater_id, ratee_id, task_id, score, comment)
    )
    return rating_id


def get_ratings_for_user(user_id):
    """Return all ratings received by a user."""
    return query_db(
        """SELECT r.*, u.name as rater_name
           FROM ratings r JOIN users u ON r.rater_id = u.id
           WHERE r.ratee_id = ?
           ORDER BY r.created_at DESC""",
        (user_id,)
    )


def has_rated(rater_id, task_id):
    """Check if a user has already rated for a specific task."""
    result = query_db(
        "SELECT id FROM ratings WHERE rater_id = ? AND task_id = ?",
        (rater_id, task_id), one=True
    )
    return result is not None
