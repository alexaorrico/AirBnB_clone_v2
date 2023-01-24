#!/usr/bin/python3
""" This module contains the places view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                    strict_slashes=False)
def handle_places(city_id):
    """ This function handles the places route """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        places = city.places
        return jsonify([place.to_dict() for place in places])
    elif request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        elif 'user_id' not in request.json:
            abort(400, 'Missing user_id')
        elif 'name' not in request.json:
            abort(400, 'Missing name')
        user = storage.get('User', request.json['user_id'])
        if not user:
            abort(404)
        place = Place(city_id=city_id, **request.json)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                    strict_slashes=False)
def handle_place(place_id):
    """ This function handles the place route """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in request.json.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                            'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
