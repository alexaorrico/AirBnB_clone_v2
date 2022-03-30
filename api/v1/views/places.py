#!/usr/bin/python3
"""
new view for Place objects that
handles all default RESTFul API actions
"""
from models.place import Place
from models import storage
from models.city import City
from api.v1.views import app_views
from flask import abort
from flask import request
from flask.json import jsonify
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_place_from_city(city_id=None):
    """
    Retrieves the list of all Place objects of a City
    """
    cities = storage.all(City)
    info = []
    if cities is not {} and city_id is not None:
        for city in cities.values():
            if city.id == city_id:
                for place in city.places:
                    info.append(place.to_dict())
                return jsonify(info)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if place is not None:
        place.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id=None):
    """
    Creates a Place
    """
    json = request.get_json(silent=True)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if json is None:
        abort(400, "Not a JSON")
    if "name" not in json:
        abort(400, "Missing name")
    if "user_id" not in json:
        abort(400, "Missing user_id")
    if storage.get(User, json["user_id"]) is None:
        abort(404)

    place = Place(**json)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    for key, value in json.items():
        if key != 'updated_at' and key != 'created_at' and key != 'id' \
                            and key != 'user_id' and key != 'city_id':
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
