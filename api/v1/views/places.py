#!/usr/bin/python3
""" retruns json response status of API """
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place

@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_cities(city_id):
    ''' gets the list of all City objects of a City '''
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    cities_list = [city.to_dict() for city in state_object.cities]
    return jsonify(cities_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    ''' gets specific place objects by its place ID '''
    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404)
    return jsonify(city_object.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    ''' deletes place object '''
    city_object = storage.get(City, city_id)
    if city_object is None:
        abort(404)
    storage.delete(city_object)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    '''' creates a place '''
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    response = request.get_json(silent=True)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in response:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_city = City(**response)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''' updates a place object '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    response = request.get_json(silent=True)
    if response is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in response.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(city.to_dict(), 200)
