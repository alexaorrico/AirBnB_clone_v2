#!/usr/bin/python3
'''city view'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def search_cities_by_id(state_id):
    '''Filter cities in state by id'''
    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    return jsonify([city.to_dict() for city in object.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def search_city_by_id(city_id):
    '''Filter city by id'''
    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_obj(city_id):
    '''Delete city of the provided id'''
    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    else:
        storage.delete(object)
        storage.save()
        # Return an empty dictionary with status code 200
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''Create a new state'''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        # method extracts and parses data from request body
        # if data is in json format, it return python dict or list
        # If the data is not valid JSON, raise an error or return None
        if 'name' not in data:
            abort(400, 'Missing name')
        new_city = City(**data)
        # Create a new instance of state and pass the key value pairs
        setattr(new_city, 'state_id', state_id)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(400, 'Not a JSON')


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Update city of provided id'''
    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(object, key, value)
    storage.save()
    return jsonify(object.to_dict()), 200