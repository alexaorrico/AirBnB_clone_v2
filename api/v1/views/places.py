#!/usr/bin/python3
from flask import jsonify, request, abort
from models import storage, Place, City
from api.v1.views import app_views


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([value.to_dict() for value in city.places])

    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'})
        elif post.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 404
        elif storage.get('User', post.get('user_id')) is None:
            abort(404)

        new_place = Place(city_id=city_id, **post)
        new_place.save()
        return jsonify(new_place.to_dict), 201

@app_views.route('/api/v1/places/<string:place_id>',
                 methods=['GET', 'DELETE', 'PUT', 'POST'], strict_slashes=False)
def get_place_id(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in put.items():
            if key not in ['id', 'created_at',
                           'updated_at', 'user_id', 'city_id']:
                setattr('place', key, value)
                storage.save()
                return jsonify(put.to_dict()), 200
