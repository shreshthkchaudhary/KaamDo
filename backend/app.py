"""KaamDo Flask Application — entry point."""
import eventlet
eventlet.monkey_patch()

import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room
from flask_jwt_extended import JWTManager

from config import Config
from models.database import init_db

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Extensions
CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Ensure upload directory exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Ensure AI models directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), 'ai', 'models'), exist_ok=True)

# Initialize database
init_db()

# ── Register blueprints ──
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.bids import bids_bp
from routes.ratings import ratings_bp
from routes.ai import ai_bp

app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(bids_bp)
app.register_blueprint(ratings_bp)
app.register_blueprint(ai_bp)


# ── Serve uploaded files ──
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)


# ── SocketIO events ──
@socketio.on('join_task')
def handle_join_task(data):
    """Client joins a task room to receive real-time bid updates."""
    task_id = data.get('task_id')
    if task_id:
        join_room(f"task_{task_id}")


@socketio.on('leave_task')
def handle_leave_task(data):
    """Client leaves a task room."""
    task_id = data.get('task_id')
    if task_id:
        leave_room(f"task_{task_id}")


# ── Health check ──
@app.route('/api/health')
def health():
    return {'status': 'ok', 'app': 'KaamDo API'}, 200


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
