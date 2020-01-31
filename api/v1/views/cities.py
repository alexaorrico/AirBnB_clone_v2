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
    """This functions lists all the cities"""
    list_t = []
    states = storage.all("State")
    s_id = "State." + state_id
    if states.get(s_id) is None:
        abort(404)
    else:
        cities = storage.all("City")
        for city in cities.values():
            if city.state_id == state_id:
                list_t.append(city.to_dict())
    return jsonify(list_t)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """This functions get a specific state by id"""
    cities = storage.all("City")
    c_id = "City." + city_id
    if cities.get(c_id) is None:
        abort(404)
    city = cities.get(c_id).to_dict()
    return city


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """This function delete a state by id"""
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
    """This function create a new city"""
    data = request.get_json()
    states = storage.all("State")
    match = "State." + state_id
    if states.get(match) is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    elif 'name' not in data:
        abort(400, 'Missing name')
    city = City()
    city.name = data['name']
    city.state_id = state_id
    city.save()
    city = city.to_dict()
    return jsonify(city), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """This function update a state by id"""
    data = request.get_json()
    cities = storage.all('City')
    match = 'City.' + city_id
    if cities.get(match) is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    else:
        city = cities.get(match)
        city.name = data['name']
        city.save()
        city = city.to_dict()
    return jsonify(city), 200
