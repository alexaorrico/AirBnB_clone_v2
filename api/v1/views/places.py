#!/usr/bin/python3
"""Amenity view model"""
from flask import abort
from flask import jsonify
from flask import request
from flask import make_response
from models import storage
from models.place import Place
from api.v1.views import app_views

place_objs = storage.all('Place')


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieves a list of all Place objects."""
    city_id = "City." + city_id

    if city_id not in storage.all('City').keys():
        abort(404)

    places = [obj.to_dict() for obj in place_objs.values()]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object."""
    place_id = "Place." + place_id

    if place_id not in place_objs.keys():
        abort(404)

    place = place_objs.get(place_id)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object."""
    place_id = "Place." + place_id

    if place_id not in place_objs.keys():
        abort(404)

    storage.all().pop(place_id)
    storage.save()

    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new Place object."""
    city_id = 'City.' + city_id

    if city_id not in storage.all('City').keys():
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "user_id" not in request.get_json().keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if "name" not in request.get_json().keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    user_id = request.get_json().get('user_id')
    user_id = 'User.' + user_id
    if user_id not in storage.all('User').keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    place = Place(**request.get_json())
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=["PUT"])
def update_place(place_id):
    """Modifies a Place object."""
    place_objs = storage.all('Place')
    place_id = "Place." + place_id

    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if place_id not in place_objs.keys():
        abort(404)
    
    place = place_objs.get(place_id)
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for k, v in request.get_json().items():
        if k not in ignored_keys:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())
