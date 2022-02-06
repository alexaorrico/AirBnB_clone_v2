#!/usr/bin/python3
""" update of ciites.py"""

from api.v1.view import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ gets cities information"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    retutn jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashe=False)
def get_city(city_id):
    """gets city info for particular city"""
    state = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city():
    """creates new city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    city = City(**request.get_json())
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """updates a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in  ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attr, val)
        city.save()
        return jsonify(city.to_dict())
        
