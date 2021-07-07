#!/usr/bin/python3
"""
Cities file for APi project
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def show_cities(state_id):
    """lists all states"""
    s_list = []
    states = storage.all("State")
    s_id = "State." + state_id
    if states.get(s_id) is None:
        abort(404)
    else:
        cities = storage.all("City")
        for city in cities.values():
            if city.state_id == state_id:
                s_list.append(city.to_dict())
    return jsonify(s_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def GetStateById(city_id):
    """Retrieves city based on its id for GET HTTP method"""
    cities = storage.all("City")
    c_id = "City." + city_id
    if cities.get(c_id) is None:
        abort(404)
    city = cities.get(c_id).to_dict()
    return city


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def DeleteStateById(city_id):
    """Deletes an state based on its id for DELETE HTTP method"""
    cities = storage.all('City')
    c_id = "City." + city_id
    to_del = cities.get(c_id)
    if to_del is None:
        abort(404)
    storage.delete(to_del)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Posts a state"""
    info = request.get_json()
    states = storage.all("State")
    pair = "State." + state_id
    if states.get(pair) is None:
        abort(404)
    if not info:
        abort(400, 'Not a JSON')
    elif 'name' not in info:
        abort(400, 'Missing name')
    city = City()
    city.name = info['name']
    city.state_id = state_id
    city.save()
    city = city.to_dict()
    return jsonify(city), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """This function update a state by id"""
    info = request.get_json()
    cities = storage.all('City')
    pair = 'City.' + city_id
    if cities.get(pair) is None:
        abort(404)
    if not info:
        abort(400, 'Not a JSON')
    else:
        city = cities.get(pair)
        city.name = info['name']
        city.save()
        city = city.to_dict()
    return jsonify(city), 200
