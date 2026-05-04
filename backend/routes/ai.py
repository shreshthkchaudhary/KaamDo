"""AI routes — classify tasks, estimate price, match workers."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ai.classifier import classify_task
from ai.price_estimator import estimate_price
from ai.match_score import calculate_match_score
from models.user import get_workers_near
from models.task import get_task_by_id

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


@ai_bp.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    description = data.get('description', '')

    if not description or len(description.strip()) < 5:
        return jsonify({'error': 'Description must be at least 5 characters'}), 400

    result = classify_task(description)
    return jsonify(result), 200


@ai_bp.route('/estimate-price', methods=['POST'])
def estimate():
    data = request.get_json()
    category = data.get('category', '')
    radius_km = data.get('radius_km', 5)

    if not category:
        return jsonify({'error': 'category is required'}), 400

    result = estimate_price(category, float(radius_km))
    return jsonify(result), 200


@ai_bp.route('/match-workers', methods=['POST'])
@jwt_required()
def match_workers():
    data = request.get_json()
    task_id = data.get('task_id')

    if not task_id:
        return jsonify({'error': 'task_id is required'}), 400

    task = get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    task_data = {
        'category': task.get('category', ''),
        'lat': task['lat'],
        'lng': task['lng'],
        'radius_km': task.get('radius_km', 5)
    }

    workers = get_workers_near(task['lat'], task['lng'], task.get('radius_km', 5))
    ranked = []

    for w in workers:
        worker_data = {
            'skills': w.get('skills', ''),
            'avg_rating': w.get('avg_rating', 0),
            'lat': w.get('lat', 0),
            'lng': w.get('lng', 0),
            'total_tasks': w.get('total_tasks', 0)
        }
        score = calculate_match_score(worker_data, task_data)
        ranked.append({
            'worker_id': w['id'],
            'name': w['name'],
            'skills': w.get('skills', ''),
            'avg_rating': w.get('avg_rating', 0),
            'total_tasks': w.get('total_tasks', 0),
            'match_score': score
        })

    ranked.sort(key=lambda x: x['match_score'], reverse=True)
    return jsonify({'workers': ranked}), 200
