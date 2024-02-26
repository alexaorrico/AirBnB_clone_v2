#!/usr/bin/python3
"""New view for Place objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.user import User
from models.place import Place

@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def get_places(city_id):
    """Retrieves the list of all Place objects of a City or creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        if 'name' not in data:
            abort(400, 'Missing name')
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def get_place(place_id):
    """Retrieves, deletes or updates a Place object"""
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
        if data is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
