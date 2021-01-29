#!/usr/bin/python3
"""Handles the user view
"""

# from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Gets the dict containing all places of a city
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.places
    places = storage.all("Places")
    list_places = []
    for user in user.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/user/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """Gets a user by its ID
    """
    user = storage.get("User", user_id)
    if user is not None:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/user/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes an user
    """
    user = storage.get("User", user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/user', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates an user
    """
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in got_json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amen = User(**got_json)
    storage.new(new_amen)
    storage.save()
    return make_response(jsonify(new_amen.to_dict()), 201)


@app_views.route('/user/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Updates an user
    """
    got_json = request.get_json()
    list_ign = ['id', 'email', 'created_at', 'updated_at']
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user = storage.get("User", user_id)
    if user:
        for key, val in got_json.items():
            setattr(user, key, val)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    else:
        abort(404)