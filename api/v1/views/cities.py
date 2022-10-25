#!/usr/bin/python3
""" Flask views for the Cities resource """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_state_cities(state_id):
    """ An endpoint that returns all cities of a state """
    rlist = []
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    else:
        cities = state.cities
        for city in cities:
            rlist.append(city.to_dict())
        return(jsonify(rlist))


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def get_city(city_id):
    """ An endpoint that returns a specific city """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """ An endpoint that deletes a specific city """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """ An endpoint that creates a specific city """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'name' not in content:
        abort(400, 'Missing name')
    new_city = City(name=content['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def modify_city(city_id):
    """ An endpoint that updats a specific city """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at', 'state_id']
    for k, v in content.items():
        if k not in ignore:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
