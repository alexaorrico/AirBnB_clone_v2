#!/usr/bin/python3
"""
Module for handling Place objects API endpoints
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def city_places(city_id):
    """Handles GET and POST requests for /cities/<city_id>/places endpoint"""
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

        user_id = data['user_id']
        user = storage.get(User, user_id)

        if user is None:
            abort(404)

        if 'name' not in data:
            abort(400, 'Missing name')

        new_place = Place(city_id=city_id, user_id=user_id, **data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def place(place_id):
    """Handles GET, DELETE, and PUT requests for /places/<place_id> endpoint"""
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
        data = request.get_json()

        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)

        place.save()
        return jsonify(place.to_dict()), 200

