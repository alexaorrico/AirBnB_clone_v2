#!/usr/bin/python3
"""
Define route for view Place
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/places/<string:place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def places(place_id=None):
    """Retrieves a Place or All the places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())


@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False, methods=['GET', 'POST'])
def place_city(city_id=None):
    """Retrieves a Place or All the places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        data = request.get_json()

        if not data:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')

        user = storage.get(User, data.get('user_id'))
        if user is None:
            abort(404)
        if 'name' not in data:
            abort(400, 'Missing name')

        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201
