#!/usr/bin/python3
"""city.py"""

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False)
def get_places_of_city(city_id=None):
    """retrieves all places in a city"""
    if storage.get(City, city_id) is None:
        abort(404)

    cities_obj = storage.all(City)

    places = storage.get(City, city_id).places
    # print(storage.get(City, city_id).places)
    # for city in cities_obj.values():
        # if city.to_dict().get('city_id') == city_id:
            # places.append(city.to_dict())
    # or we can do
    # cities = [city.to_dict() for city in cities_obj.values()
    # if city.to_dict().get('city_id') == city_id]

    return jsonify(places), 200


@app_views.route("/places/<string:place_id>")
def get_place(place_id=None):
    """retrieves a specific place """
    if place_id is None:
        abort(404)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=['DELETE'])
def delete_place(place_id=None):
    """Deletes a specific place """
    if place_id is None:
        abort(404)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route(
        "/cities/<string:city_id>/places",
        methods=['POST'],
        strict_slashes=False)
def create_place(city_id=None):
    """ Creates a place"""
    if storage.get(City, city_id) is None:
        return jsonify({"error": "Not found"}), 404

    place_dict = None
    try:
        place_dict = request.get_json()
        if not isinstance(place_dict, dict):
            raise ValueError
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in place_dict:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in place_dict:
        return jsonify({"error": "Missing name"}), 400

    if storage.get(User, place_dict['user_id']) is None:
        return jsonify({"error": "Not found"}), 404

    place = Place()
    for key, val in place_dict.items():
        setattr(place, key, val)

    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """ updates a place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_dict = None
    try:
        place_dict = request.get_json()
        if not isinstance(place_dict, dict):
            raise ValueError
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, val in place_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, val)

    storage.save()
    return jsonify(place.to_dict()), 200
