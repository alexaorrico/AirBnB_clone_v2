from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_or_add_user():
    """Get all users or add a new user."""
    if request.method == 'GET':
        users = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users), 200
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'JSON data is required')
        email = data.get("email")
        password = data.get('password')
        if not email:
            abort(400, 'Missing email')
        if not password:
            abort(400, 'Missing password')
        new_user = User(**data)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_by_id(user_id):
    """Get, delete, or update a user by ID."""
    user_data = storage.get(User, user_id)
    if not user_data:
        abort(404)
    if request.method == 'GET':
        return jsonify(user_data.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(user_data)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'JSON data is required')
        for k, v in data.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user_data, k, v)
        storage.save()
        return jsonify(user_data.to_dict()), 200
