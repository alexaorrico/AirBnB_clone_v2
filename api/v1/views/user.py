#!/usr/bin/python3
"""View of Cities for RESTFul API"""

from api.v1.views import app_views, validate_model, get_json
from flask import jsonify
from models import storage, class_dictionary
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all USER objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves the list of all USER objects"""
    user = validate_model("User", user_id)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a City object"""
    user = validate_model("User", user_id)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """User no ID given POST scenario"""
    req_json = get_json(['email', 'password'])
    User = class_dictionary.get('User')
    new_object = User(**req_json)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """User with ID given PUT scenario"""
    user_obj = validate_model("User", user_id)
    req_json = get_json()
    for key, value in req_json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict())
