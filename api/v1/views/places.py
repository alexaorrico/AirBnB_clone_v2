#!/usr/bin/python3
""" retruns json response status of API """
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    ''' Retrieves the list of all Place objects of a City '''
    city_id = storage.get(City, city_id)
    if city_id is None:
        abort(404)
    places_list = [place.to_dict() for place in city_id.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    ''' gets specific place objects by its place ID '''
    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404)
    return jsonify(place_object.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    ''' deletes place object '''
    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404)
    storage.delete(place_object)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    '''' creates a place '''
    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404)

    response = request.get_json(silent=True)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in response:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    user_id = storage.get(User, response['user_id'])
    if user_id is None:
        abort(404)

    if 'name' not in response:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_place = Place(**response)
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''' updates a place object '''
    place_id = storage.get(Place, place_id)
    if place_id is None:
        abort(404)
    response = request.get_json(silent=True)
    if response is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in response.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_id, key, value)
    storage.save()
    return make_response(place_id.to_dict(), 200)
