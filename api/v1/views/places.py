#!/usr/bin/python3

""" Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_by_city(city_id):
    """retrieve places based on city_id"""

    if request.method == 'GET':
        city = storage.get(City, city_id)

        if city:
            places = [place.to_dict() for place in city.places]
            return jsonify(places)
        abort(404)
    elif request.method == 'POST':
        city = storage.get(City, city_id)

        if city:
            my_dict = request.get_json()
            if my_dict is None:
                abort(400, 'Not a JSON')
            if my_dict.get("user_id") is None:
                abort(400, 'Missing user_id')
            if my_dict.get("name") is None:
                abort(400, 'Missing name')

            user = storage.get(User, my_dict.get("user_id"))

            if user:
                place = Place(**my_dict)
                place.save()
                return jsonify(place.to_dict()), 201
            abort(404)
        abort(404)


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place_by_place_id(place_id):
    """Retrieves a place based on the place_id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        my_dict = request.get_json()
        if my_dict is None:
            abort(400, 'Not a JSON')
        for k, v in my_dict.items():
            setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200
