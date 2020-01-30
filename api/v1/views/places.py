#!/usr/bin/python3
"""
Define user endpoints
"""
from models import storage
from Flask import request, jsonify, abort
from api.v1.views import app_views
from models.city import City
from models.places import Place


@app_views.route('/cities/<city_id/places', strict_slashes=False,
                 methods=['GET'])
def get_city_places(city_id):
    """retrieve all places in a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place_by_id(place_id):
    """get place by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return place.to_dict()


@app_views.route('/places/<place_id>')
def delete_place(place_id):
    """delete city by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def post_city_places(city_id):
    """create places with city id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    if "user_id" not in json_data:
        return "Missing user_id", 400
    if "name" not in json_data:
        return "Missing name", 400
    if json_data["user_id"] is None:
        abort(404)
    json_data["city_id"] = city_id
    new_place = Place(**json_data)
    new_place.save()
    return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """update place by id"""
    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    for key in json_data:
        if key not in ignore:
            setattr(place, key, json_data[key])
    storage.save()
    return place.to_dict(), 200
