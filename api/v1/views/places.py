#!/usr/bin/python3
"""Module to create a new view for Place objects"""
from flask import jsonify, Flask, request, abort
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city_id(city_id):
    """Retrieves the list of all Place objects by city_id"""
    city = storage.get('City', city_id)
    list_of_places = []
    if city is None:
        return jsonify({"error": "Not found"}), 404
    for element in city.places:
        list_of_places.append(element.to_dict())
    return jsonify(list_of_places)


@app_views.route('places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """Retrieves the list of all Place objects of a City by city_id"""
    place = storage.get('Place', place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Deletes a place by ID"""
    place = storage.get('Place', place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Post a Place object"""
    data = request.get_json()
    city = storage.get('City', city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    if 'user_id' not in data:
        abort(400)
        abort(Response("Missing user_id"))
    if 'name' not in data:
        abort(400)
        abort(Response("Missing name"))

    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Put a Place object"""
    place = storage.get('Place', place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))

    # TODO:
    # Ignore id, city_id, created_at and updated_at
    for k, v in data.items():
        setattr(place, k, v)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 200
