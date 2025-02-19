#!/usr/bin/python3
'''states file'''
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_state(state_id):
    '''return cities of a state'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City)
    cities_state = []
    for city in cities.values():
        if city.state_id == state.id:
            cities_state.append(city.to_dict())
    return jsonify(cities_state)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/states/citie/<city_id>',
                 methods=['GET'], strict_slashes=False)
def req_city(city_id):
    '''return a specific city'''
    try:
        city = storage.get(City, city_id)
    except KeyError:
        abort(404)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    '''delete a specific city'''
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    '''post a city'''
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    try:
        state = storage.get(State, state_id)
    except KeyError:
        abort(404)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    name = data.get('name')
    if name is None:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT', 'GET'], strict_slashes=False)
def update_city(city_id):
    '''update a city'''
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    try:
        city = storage.get(City, city_id)
    except KeyError:
        abort(404)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
