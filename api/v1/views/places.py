#!/usr/bin/python3
"""This view implements the RESTful API operations for `Place` objects"""
from flask import jsonify, abort, request, make_response
from . import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def read_places(city_id):
    """Retrieves the list of all `Place` objects of a city"""

    if storage.get(City, city_id) is None:
        abort(404)

    places = storage.all(Place).values()
    return jsonify([
        place.to_dict() for place in places if place.city_id == city_id
    ])


@app_views.route('/places/<place_id>', methods=['GET'])
def read_place(place_id):
    """Retrieves the `Place` object with the given `place_id`"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes the `Place` object with the given `place_id`"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new `Place` object associated with the given `city_id`"""
    if storage.get(City, city_id) is None:
        abort(404)

    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, "Not a JSON")
    if "user_id" not in place_data:
        abort(400, "Missing user_id")

    user_id = place_data["user_id"]
    if storage.get(User, user_id) is None:
        abort(404)

    if "name" not in place_data:
        abort(400, "Missing name")

    place_data["city_id"] = city_id
    allowed = (
        "city_id", "user_id", "name", "description", "number_rooms",
        "number_bathrooms", "max_guest", "price_by_night",
    )

    new_place = Place()
    for key, value in place_data.items():
        if key in allowed:
            setattr(new_place, key, value)

    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates the `Place` object with the given `place_id`"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, "Not a JSON")

    allowed = (
        "name", "description", "number_rooms", "number_bathrooms",
        "max_guest", "price_by_night",
    )

    for key, value in place_data.items():
        if key in allowed:
            setattr(place, key, value)

    place.save()
    return make_response(jsonify(place.to_dict()), 200)
