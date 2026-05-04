"""User model helpers."""

from werkzeug.security import generate_password_hash, check_password_hash
from models.database import query_db, execute_db


def create_user(name, email, password, role, skills=None, lat=None, lng=None):
    """Create a new user and return their id."""
    password_hash = generate_password_hash(password)
    user_id = execute_db(
        """INSERT INTO users (name, email, password_hash, role, skills, lat, lng)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (name, email, password_hash, role, skills, lat, lng)
    )
    return user_id


def get_user_by_email(email):
    """Look up a user by email."""
    return query_db("SELECT * FROM users WHERE email = ?", (email,), one=True)


def get_user_by_id(user_id):
    """Look up a user by id."""
    return query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)


def verify_password(stored_hash, password):
    """Check a plaintext password against the stored hash."""
    return check_password_hash(stored_hash, password)


def update_user_rating(user_id):
    """Recalculate avg_rating for a user from all their received ratings."""
    result = query_db(
        "SELECT AVG(score) as avg, COUNT(*) as cnt FROM ratings WHERE ratee_id = ?",
        (user_id,), one=True
    )
    if result and result['avg']:
        execute_db(
            "UPDATE users SET avg_rating = ? WHERE id = ?",
            (round(result['avg'], 2), user_id)
        )


def update_user_tasks(user_id):
    """Increment total_tasks count for a user."""
    execute_db(
        "UPDATE users SET total_tasks = total_tasks + 1 WHERE id = ?",
        (user_id,)
    )


def get_workers_near(lat, lng, radius_km):
    """Return all workers (no spatial index — fine for SQLite dev)."""
    return query_db("SELECT * FROM users WHERE role = 'worker'")


def safe_user_dict(user):
    """Return user dict without password_hash."""
    if user is None:
        return None
    u = dict(user) if not isinstance(user, dict) else user.copy()
    u.pop('password_hash', None)
    return u
