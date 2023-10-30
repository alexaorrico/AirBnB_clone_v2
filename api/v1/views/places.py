#!/usr/bin/python3
"""Import required modules"""
from flask import Flask, make_response
from flask import abort, jsonify, request
from models.place import Place
from os import getenv
import json
from api.v1.views import app_views


host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_list_of_all_places(city_id):
    """Retrieves the list of all Place objects"""
    from models import storage
    storage.reload
    places_obj = storage.all(Place).values()
    city_places = []
    for place in places_obj:
        if place.city_id == city_id:
            city_places.append(place)
    if len(city_places) >= 1:
        places_dict = [place_obj.to_dict() for place_obj in city_places]
        return jsonify(places_dict)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_obj(place_id):
    """Retrieves a State object"""
    from models import storage
    storage.reload
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_ob(place_id):
    """Deletes a Place object"""
    from models import storage
    storage.reload
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    try:
        data = request.get_json()
    except Exception:
        return jsonify("Not a JSON"), 400
    if 'user_id' not in data:
        return jsonify("Missing user_id"), 400
    if 'name' not in data:
        return jsonify("Missing name"), 400
    from models import storage
    if not storage.get(City, city_id):
        abort(404)
    if not storage.get(User, user_id):
        abort(404)
    new_place = Place(**data)
    setattr(new_place, 'city_id', city_id)
    new_place.save()
    return (new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a State object"""
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'Not a JSON'}), 400

    from models import storage
    place = storage.get(Place, place_id)
    if place:
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return (place.to_dict())
    abort(404)  # If no matching place is found, return a 404 error
