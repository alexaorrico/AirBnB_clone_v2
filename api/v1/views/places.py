#!/usr/bin/python3
""" A new view for Place objects that handles all
    default RESTFul API actions """

from models import storage
from models.city import City
from models.user import User
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def place_in_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        user_id = request.json['user_id']
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        new_place = Place(**request.get_json())
        new_place.city_id = city_id
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place(place_id):
    """Retrieves a Place object using place id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.json.items():
            if k not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(place, k, v)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)
