#!/usr/bin/python3
"""This module is in charge of handling requests for state-type objects."""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models import City


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def return_cities(state_id):
    '''return list of all the cities associated with the state_id'''
    if storage.get('State', state_id) is None:
        abort(404)
    all_cities = storage.all('City')
    new_cities = []
    for key, val in all_cities.items():
        if state_id == val.state_id:
            new_cities.append(val.to_dict())
    return jsonify(new_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def return_city(city_id):
    """Get a specific City object through the HTTP GET request"""
    try:
        city_obj = storage.get('City', city_id)
        if city_obj is not None:
            return jsonify(city_obj.to_dict())
        abort(404)
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''Delete a specific City object through the HTTP DELETE request'''
    try:
        city_obj = storage.get('City', city_id)
        if city_obj is None:
            abort(404)
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False)
def post_city(state_id):
    '''Create a new City object through the HTTP POST request'''
    try:
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in request.json:
            return jsonify({'error': 'Missing name'}), 400
        new_city = request.get_json().get('name')
        state_obj = storage.get('State', state_id)
        if state_obj is None:
            abort(404)

        new_obj = City(name=new_city, state_id=state_id)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id):
    '''Update a specific City object through the HTTP PUT request'''
    try:
        city_obj = storage.get('City', city_id)
        if city_obj is None:
            abort(404)
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400

        new_attrs = request.get_json()
        dont_add = {'id', 'created_at', 'updated_at'}
        for key, value in new_attrs.items():
            if key not in dont_add:
                setattr(city_obj, key, value)
        city_obj.save()
        return jsonify(city_obj.to_dict()), 200
    except Exception:
        abort(404)
