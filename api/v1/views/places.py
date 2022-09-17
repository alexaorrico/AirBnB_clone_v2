#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_get():
    """Retrieves the list of all Place"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)

    places_list = []
    all_places = storage.all(Place)
    for key, value in all_places.items():
        places_list.append(value.to_dict())
    return jsonify(places_list)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_post():
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)

    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    if 'user_id' not in transform_dict.keys():
        abort(400, "Missing user_id")

    user_id = storage.get(User, dico['user_id'])
    if user_id is None:
        return abort(404)
    if 'name' not in transform_dict.keys():
        abort(400, "Missing name")
    else:
        dico['city_id'] = city_id
        new_place = Place(**transform_dict)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id_get(place_id):
    """Retrieves a Place object and 404 if it's an error"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_id_delete(place_id):
    """Deletes a Place object and 404 if it's an error"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_id_put(place_id):
    """Updates a Place object"""
    ignore_list = ['id', 'created_at', 'user_id', 'city_id', 'updated_at']
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    for key, value in transform_dict.items():
        if key not in ignore_list:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
