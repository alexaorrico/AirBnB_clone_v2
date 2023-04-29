from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', strict_slashes=False)
def get_users():
    """get all users"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """get a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create a user"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())



