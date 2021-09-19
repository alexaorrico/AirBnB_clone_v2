#!/usr/bin/python3
""" Routes for states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import user
from models.user import User


@app_views.route('/users', methods=["GET"], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def users(user_id=None):
    """Get specific id user or all users"""
    if user_id is None:
        users = storage.all("User")
        all_users = [value.to_dict() for key, value in users.items()]
        return jsonify(all_users), 200
    all_users = storage.get(User, user_id)
    if all_users is None:
        abort (404)
    return jsonify(all_users.to_dict()), 200
    

@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User based on ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def post_user():
    """Creates user"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "email" not in data.keys():
        abort(400, "Missing email")
    if "password" not in data.keys():
        abort(400, "Missing password")
    
    new_data = User(**data)
    new_data.save()
    return (jsonify(new_data.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """Updates User id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key in ['id', 'email', 'created_at', 'updated_at']:
            continue
        else:
            setattr(user, key, value)
    user.save()
    return (jsonify(user.to_dict()), 200)
