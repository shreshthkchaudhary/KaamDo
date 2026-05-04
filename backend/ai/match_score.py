"""Worker Match Score — weighted formula (no ML model needed).

Ranks workers by skill fit, rating, proximity, and experience.
"""

import math


def haversine(lat1, lng1, lat2, lng2):
    """Calculate the great-circle distance between two points on Earth (km)."""
    R = 6371  # Earth radius in km
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def calculate_match_score(worker, task):
    """Return a 0–100 match score for a worker–task pair.

    Weights:
        Category match  40%
        Rating          30%
        Proximity       20%
        Experience      10%
    """
    # Category match: full match if task category appears in worker skills
    worker_skills = (worker.get('skills') or '').lower()
    task_category = (task.get('category') or '').lower()
    category_match = 1.0 if task_category and task_category in worker_skills else 0.3

    # Rating score (0–1)
    rating_score = (worker.get('avg_rating') or 0) / 5.0

    # Proximity score — closer is better
    w_lat = worker.get('lat') or 0
    w_lng = worker.get('lng') or 0
    t_lat = task.get('lat') or 0
    t_lng = task.get('lng') or 0
    radius = task.get('radius_km') or 5

    if w_lat and w_lng and t_lat and t_lng:
        distance = haversine(w_lat, w_lng, t_lat, t_lng)
        proximity_score = max(0, 1 - (distance / radius))
    else:
        proximity_score = 0.5  # Unknown location, give neutral score

    # Task experience score
    total = worker.get('total_tasks') or 0
    task_exp_score = min(total / 100, 1.0)

    score = (
        category_match  * 0.40 +
        rating_score    * 0.30 +
        proximity_score * 0.20 +
        task_exp_score  * 0.10
    )

    return round(score * 100, 1)
