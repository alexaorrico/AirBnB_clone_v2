#!/usr/bin/python3
""" API for retriving all Users """
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """Creates a User"""
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route(
        "/users/<user_id>/places", strict_slashes=False, methods=["GET"])
def get_user_places(user_id):
    """Retrieves the list of all Place objects of a User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify([place.to_dict() for place in user.places])


@app_views.route(
        "/users/<user_id>/places", strict_slashes=False, methods=["POST"])
def create_user_place(user_id):
    """Creates a Place"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    if 'city_id' not in data:
        abort(400, "Missing city_id")
    city = storage.get(City, data['city_id'])
    if not city:
        abort(404)
    data['user_id'] = user_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)
