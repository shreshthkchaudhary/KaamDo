"""Rating routes — submit and view ratings."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.rating import create_rating, get_ratings_for_user, has_rated
from models.user import get_user_by_id, update_user_rating
from models.task import get_task_by_id

ratings_bp = Blueprint('ratings', __name__)


@ratings_bp.route('/api/ratings', methods=['POST'])
@jwt_required()
def submit_rating():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    required = ['ratee_id', 'task_id', 'score']
    for field in required:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    ratee_id = data['ratee_id']
    task_id = data['task_id']
    score = data['score']

    if not isinstance(score, int) or score < 1 or score > 5:
        return jsonify({'error': 'Score must be an integer between 1 and 5'}), 400

    if user_id == ratee_id:
        return jsonify({'error': 'Cannot rate yourself'}), 400

    task = get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    if task['status'] != 'completed':
        return jsonify({'error': 'Can only rate after task is completed'}), 400

    if has_rated(user_id, task_id):
        return jsonify({'error': 'You have already rated for this task'}), 409

    rating_id = create_rating(
        rater_id=user_id,
        ratee_id=ratee_id,
        task_id=task_id,
        score=score,
        comment=data.get('comment')
    )

    # Recalculate average rating for the ratee
    update_user_rating(ratee_id)

    return jsonify({'message': 'Rating submitted', 'rating_id': rating_id}), 201


@ratings_bp.route('/api/users/<int:user_id>/ratings', methods=['GET'])
def user_ratings(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    ratings = get_ratings_for_user(user_id)
    return jsonify({'ratings': ratings, 'avg_rating': user['avg_rating']}), 200
