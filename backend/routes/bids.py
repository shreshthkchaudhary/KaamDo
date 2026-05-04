"""Bid routes — create, list, accept bids."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.bid import create_bid, get_bids_for_task, get_bid_by_id, accept_bid, get_bids_by_worker
from models.task import get_task_by_id, update_task_status
from models.user import get_user_by_id
from ai.match_score import calculate_match_score

bids_bp = Blueprint('bids', __name__)


@bids_bp.route('/api/bids', methods=['POST'])
@jwt_required()
def place_bid():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)

    if not user or user['role'] != 'worker':
        return jsonify({'error': 'Only workers can place bids'}), 403

    data = request.get_json()
    task_id = data.get('task_id')
    amount = data.get('amount')

    if not task_id or not amount:
        return jsonify({'error': 'task_id and amount are required'}), 400

    task = get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    if task['status'] != 'open':
        return jsonify({'error': 'Task is no longer accepting bids'}), 400

    # Calculate match score
    worker_data = {
        'skills': user.get('skills', ''),
        'avg_rating': user.get('avg_rating', 0),
        'lat': user.get('lat', 0),
        'lng': user.get('lng', 0),
        'total_tasks': user.get('total_tasks', 0)
    }
    task_data = {
        'category': task.get('category', ''),
        'lat': task['lat'],
        'lng': task['lng'],
        'radius_km': task.get('radius_km', 5)
    }
    match = calculate_match_score(worker_data, task_data)

    bid_id = create_bid(
        task_id=task_id,
        worker_id=user_id,
        amount=float(amount),
        message=data.get('message'),
        match_score=match
    )

    bid = get_bid_by_id(bid_id)
    bid_dict = dict(bid)
    bid_dict['worker_name'] = user['name']
    bid_dict['worker_rating'] = user['avg_rating']

    # Emit real-time event (SocketIO import is done in app.py)
    try:
        from app import socketio
        socketio.emit('new_bid', bid_dict, room=f"task_{task_id}")
    except Exception:
        pass  # SocketIO not available in testing

    return jsonify({'bid': bid_dict}), 201


@bids_bp.route('/api/tasks/<int:task_id>/bids', methods=['GET'])
def get_task_bids(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    bids = get_bids_for_task(task_id)
    return jsonify({'bids': bids}), 200


@bids_bp.route('/api/bids/<int:bid_id>/accept', methods=['PATCH'])
@jwt_required()
def accept_a_bid(bid_id):
    user_id = int(get_jwt_identity())

    bid = get_bid_by_id(bid_id)
    if not bid:
        return jsonify({'error': 'Bid not found'}), 404

    task = get_task_by_id(bid['task_id'])
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    if task['poster_id'] != user_id:
        return jsonify({'error': 'Only the poster can accept bids'}), 403
    if task['status'] != 'open':
        return jsonify({'error': 'Task is no longer open'}), 400

    accept_bid(bid_id)
    update_task_status(bid['task_id'], 'assigned')

    # Emit escrow event
    try:
        from app import socketio
        socketio.emit('bid_accepted', {
            'bid_id': bid_id,
            'task_id': bid['task_id'],
            'amount': bid['amount']
        }, room=f"task_{bid['task_id']}")
    except Exception:
        pass

    return jsonify({'message': 'Bid accepted, task assigned', 'escrow_amount': bid['amount']}), 200


@bids_bp.route('/api/bids/my', methods=['GET'])
@jwt_required()
def my_bids():
    user_id = int(get_jwt_identity())
    bids = get_bids_by_worker(user_id)
    return jsonify({'bids': bids}), 200
