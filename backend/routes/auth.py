"""Authentication routes — register, login, get current user."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import create_user, get_user_by_email, get_user_by_id, verify_password, safe_user_dict

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    required = ['name', 'email', 'password', 'role']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400

    if data['role'] not in ('poster', 'worker'):
        return jsonify({'error': 'role must be poster or worker'}), 400

    # Check if email already exists
    if get_user_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 409

    try:
        user_id = create_user(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role=data['role'],
            skills=data.get('skills'),
            lat=data.get('lat'),
            lng=data.get('lng')
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    token = create_access_token(identity=str(user_id))
    user = safe_user_dict(get_user_by_id(user_id))

    return jsonify({'token': token, 'user': user}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = get_user_by_email(data['email'])
    if not user or not verify_password(user['password_hash'], data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = create_access_token(identity=str(user['id']))
    return jsonify({'token': token, 'user': safe_user_dict(user)}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': safe_user_dict(user)}), 200
