"""Task routes — CRUD + nearby filtering."""

import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models.task import (create_task, get_task_by_id, get_all_tasks,
                         get_tasks_by_poster, update_task_status)
from models.user import get_user_by_id, update_user_tasks
from ai.match_score import haversine

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_new_task():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)

    if not user or user['role'] != 'poster':
        return jsonify({'error': 'Only posters can create tasks'}), 403

    # Handle both JSON and form-data (for file uploads)
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = request.form.to_dict()
        photo = request.files.get('photo')
    else:
        data = request.get_json()
        photo = None

    required = ['title', 'description', 'budget', 'lat', 'lng']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400

    photo_path = None
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        upload_dir = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        photo_path = os.path.join(upload_dir, filename)
        photo.save(photo_path)
        photo_path = filename  # Store only the filename

    task_id = create_task(
        poster_id=user_id,
        title=data['title'],
        description=data['description'],
        category=data.get('category'),
        budget=float(data['budget']),
        lat=float(data['lat']),
        lng=float(data['lng']),
        radius_km=float(data.get('radius_km', 5)),
        suggested_min=data.get('suggested_price_min'),
        suggested_max=data.get('suggested_price_max'),
        photo_path=photo_path
    )

    task = get_task_by_id(task_id)
    return jsonify({'task': dict(task)}), 201


@tasks_bp.route('', methods=['GET'])
def get_tasks():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', default=10, type=float)

    all_tasks = get_all_tasks()

    if lat is not None and lng is not None:
        # Filter by distance
        nearby = []
        for t in all_tasks:
            dist = haversine(lat, lng, t['lat'], t['lng'])
            t_copy = dict(t)
            t_copy['distance_km'] = round(dist, 2)
            if dist <= radius:
                nearby.append(t_copy)
        nearby.sort(key=lambda x: x['distance_km'])
        return jsonify({'tasks': nearby}), 200

    return jsonify({'tasks': all_tasks}), 200


@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_single_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Include poster info
    poster = get_user_by_id(task['poster_id'])
    task_dict = dict(task)
    task_dict['poster_name'] = poster['name'] if poster else 'Unknown'
    task_dict['poster_rating'] = poster['avg_rating'] if poster else 0

    return jsonify({'task': task_dict}), 200


@tasks_bp.route('/<int:task_id>/status', methods=['PATCH'])
@jwt_required()
def change_task_status(task_id):
    user_id = int(get_jwt_identity())
    task = get_task_by_id(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404
    if task['poster_id'] != user_id:
        return jsonify({'error': 'Only the poster can update task status'}), 403

    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ('assigned', 'completed', 'cancelled'):
        return jsonify({'error': 'Invalid status'}), 400

    update_task_status(task_id, new_status)

    # If task completed, increment total_tasks for both poster and worker
    if new_status == 'completed':
        update_user_tasks(user_id)
        # Find accepted worker
        from models.bid import get_bids_for_task
        bids = get_bids_for_task(task_id)
        for bid in bids:
            if bid['status'] == 'accepted':
                update_user_tasks(bid['worker_id'])
                break

    return jsonify({'message': f'Task status updated to {new_status}'}), 200
