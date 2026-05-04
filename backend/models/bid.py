"""Bid model helpers."""

from models.database import query_db, execute_db


def create_bid(task_id, worker_id, amount, message=None, match_score=None):
    """Insert a new bid and return its id."""
    bid_id = execute_db(
        """INSERT INTO bids (task_id, worker_id, amount, message, match_score)
           VALUES (?, ?, ?, ?, ?)""",
        (task_id, worker_id, amount, message, match_score)
    )
    return bid_id


def get_bids_for_task(task_id):
    """Return all bids on a task, with worker info."""
    return query_db(
        """SELECT b.*, u.name as worker_name, u.avg_rating as worker_rating,
                  u.skills as worker_skills, u.total_tasks as worker_total_tasks
           FROM bids b JOIN users u ON b.worker_id = u.id
           WHERE b.task_id = ?
           ORDER BY b.match_score DESC NULLS LAST, b.created_at ASC""",
        (task_id,)
    )


def get_bid_by_id(bid_id):
    """Return a single bid."""
    return query_db("SELECT * FROM bids WHERE id = ?", (bid_id,), one=True)


def accept_bid(bid_id):
    """Mark a bid as accepted and reject all other bids on the same task."""
    bid = get_bid_by_id(bid_id)
    if not bid:
        return False
    # Accept this bid
    execute_db("UPDATE bids SET status = 'accepted' WHERE id = ?", (bid_id,))
    # Reject all other pending bids on this task
    execute_db(
        "UPDATE bids SET status = 'rejected' WHERE task_id = ? AND id != ? AND status = 'pending'",
        (bid['task_id'], bid_id)
    )
    return True


def get_bids_by_worker(worker_id):
    """Return all bids placed by a worker."""
    return query_db(
        """SELECT b.*, t.title as task_title, t.status as task_status,
                  t.budget as task_budget
           FROM bids b JOIN tasks t ON b.task_id = t.id
           WHERE b.worker_id = ?
           ORDER BY b.created_at DESC""",
        (worker_id,)
    )
