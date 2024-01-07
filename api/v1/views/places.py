#!/usr/bin/python3
""" Place objects """
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """Create a new view for City objects that handles all default
    RestFul API actions.
    """
    city = storage.get('City', city_id)
    print(city)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in city.places])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        elif post.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400
        elif storage.get('User', post.get('user_id')) is None:
            abort(404)
        new_place = Place(city_id=city_id, **post)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_place_id(place_id):
    """Retrieves a city object with a specific id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        place = storage.get('Place', place_id)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'city_id', 'user_id']:
                setattr(place, key, value)
                storage.save()
        return jsonify(place.to_dict()), 200
