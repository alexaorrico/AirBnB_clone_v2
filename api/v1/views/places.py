#!/usr/bin/python3
"""Handles the user view
"""

# from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Gets the dict containing all places of a city
    """
    city = storage.get("City", city_id)
    if city is None:
        return abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """Gets a place by its ID
    """
    place = storage.get("Place", place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place
    """
    place = storage.get("Place", place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a place
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in got_json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    a_user = storage.get("User", got_json['user_id'])
    if a_user is None:
        abort(404)
    if 'name' not in got_json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_place = Place(**got_json)
    storage.new(new_place)
    new_place.city_id = city.id
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates an place
    """
    got_json = request.get_json()
    list_ign = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    place = storage.get("Place", place_id)
    if place:
        for key, val in got_json.items():
            setattr(place, key, val)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    else:
        abort(404)
