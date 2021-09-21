#!/usr/bin/python3
"""
script that starts a Flask web application:
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, place
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def place_all(city_id):
    """
    Retrieves a city object:
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    list = []
    for place in city.places:
        list.append(place.to_dict())
    return jsonify(list)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def plac_all(place_id):
    """
    Retrieves a place object:
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """
    Deletes a place object
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """
    Creates a Place
    """

    my_place = request.get_json()
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json().keys():
        abort(400, "Missing user_id")
    if "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        my_place['city_id'] = city_id
        plaace = Place(**my_place)
        plaace.save()
        resp = jsonify(plaace.to_dict())
        return (resp), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def place_put(place_id):
    """
    Updates a place object
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    my_place = request.get_json()
    if my_place is None:
        abort(400, "Not a JSON")
    else:
        for key, value in my_place.items():
            if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(place, key, value)
        storage.save()
        resp = place.to_dict()
        return jsonify(resp), 200
