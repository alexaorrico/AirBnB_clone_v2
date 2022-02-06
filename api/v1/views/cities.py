#!/usr/bin/python3
"""cities routes"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False)
def cities(state_id):
    """list all cities by state"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404, 'Not found')
    cities = [obj.to_dict() for obj in (storage.all('City')).values()
              if obj.state_id == state_id]
    return jsonify(cities), 200


@app_views.route('/cities/<string:city_id>', strict_slashes=False)
def city_id(city_id):
    """json data of a single city"""
    city = storage.get('City', city_id)
    if city:
        return jsonify(city.to_dict()), 200
    abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete json data of a single city"""
    city = storage.get('City', city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({})
    abort(404, 'Not found')


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create a new city"""
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a JSON')
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if dictionary.get('name') is None:
        abort(400, 'Missing name')
    dictionary['state_id'] = state_id
    city = City(**dictionary)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update data of city"""
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a JSON')
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    [setattr(city, key, value) for key, value in dictionary.items()
     if key not in ['id', 'state_id', 'created_at', 'updated_at']]
    city.save()
    return jsonify(city.to_dict()), 200
