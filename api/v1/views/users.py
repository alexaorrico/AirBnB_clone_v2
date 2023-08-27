from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users = User.get_all()
    return jsonify([user.to_dict() for user in users]), 200

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = User.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = User.get(user_id)
    if not user:
        abort(404)
    user.delete()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = User.get(user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
