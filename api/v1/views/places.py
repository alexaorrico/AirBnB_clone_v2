#!/usr/bin/python3
"""
handles all default RestFul API actions for places
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request
from flask import abort
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    ge the places by city id
    """
    list_objects = []

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = storage.all(Place)
    for place in places.values():
        if place.city_id == city.id:
            list_objects.append(place.to_dict())
    return jsonify(list_objects)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_places_by_id(place_id):
    """
    get the places by id
    """
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)

    return jsonify(places.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """
    delete places by id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_places(city_id):
    """
    create places by city id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        abort(400, "Not a JSON")

    if "user_id" not in json_data:
        abort(400, "Missing user_id")

    user = storage.get(User, json_data.get("user_id"))
    if user is None:
        abort(404)

    if "name" not in json_data:
        abort(404, "Missing name")

    json_data["city_id"] = city_id
    new_place = Place(**json_data)
    storage.new(new_place)
    storage.save()

    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_places(place_id):
    """
    Update places by id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        abort(404, "Not a JSON")

    for key, value in json_data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
