#!/usr/bin/python3
"""creates a new view for User objects"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort


@app_views.route('/users/', methods=["GET"],
                 strict_slashes=False)
def city_list(user_id):
    """retrieves all user objects"""
    user_list = []
    userstorage = list(storage.all("User").values())
    for userobj in userstorage:
        user_list.append(userobj.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=["GET"],
                 strict_slashes=False)
def city_list(user_id):
    """retrieves a user object"""
    try:
        userobj = storage.get(User, user_id).to_dict()
        return jsonify(userobj)
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def city(user_id):
    """deletes a user object"""
    userobj = storage.get(Amenity, amenity_id)
    if userobj is not None:
        storage.delete(userobj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/users/', methods=["POST"],
                 strict_slashes=False)
def create():
    """creates a user object"""
    try:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        body_dict = request.get_json()
        if "email" not in body_dict:
            return jsonify({"error": "Missing email"}), 400
        if "password" not in body_dict:
            return jsonify({"error": "Missing password"}), 400
        userobj = User(email=body_dict["email"],
                       password=body_dict["password"])
        userobj.save()
        return jsonify(userobj.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update(user_id):
    """updates existing user object"""
    userobj = storage.get(User, user_id)
    if userobj is None:
        abort(404)
    body_dict = request.get_json()
    if body_dict is None:
        abort(400, "Not a JSON")
    body_dict.pop("id", None)
    body_dict.pop("email", None)
    body_dict.pop("created_at", None)
    body_dict.pop("updated_at", None)
    for key, value in body_dict.items():
        setattr(userobj, key, value)
    userobj.save()
    return jsonify(userobj.to_dict()), 200
