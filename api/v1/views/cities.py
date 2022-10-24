#!/usr/bin/python3
"""
view for city  objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State

# states = []
# cities = []
# states_dict = storage.all(State)
# cities_dict = storage.all(City)
# for k, v in states_dict.items():
#     states.append(v.to_dict())
# for k, v in cities_dict.items():
#     cities.append(v.to_dict())


@app_views.route('/states/<state_id>/cities')
def cities_in_state(state_id):
    """Retrieves the list of all State objects """
    state = storage.get(State, state_id)
    cities = storage.all(City)
    if not state:
        abort(404)
    state_cities = [
        city.to_dict()
        for city in cities.values() if city.state_id == state_id
        ]
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>')
def get_cities(city_id):
    """"Retrieves the list of all City objects """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city Object"""
    city = storage.get(City, city_id)
    all_cities = storage.all(City)
    if not city:
        abort(404)
    for k, v in all_cities.items():
        if v.id == city_id:
            v.delete()
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """creates a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    if 'name' not in request.get_json():
        return ("Missing name\n", 400)
    request_data = request.get_json()
    request_data['state_id'] = state_id
    new_city = City(**request_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """updates a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
        # return (jsonify(error="Not a JSON"), 400)
    request_data = request.get_json()
    request_data.pop('id', None)
    request_data.pop('created_at', None)
    request_data.pop('updated_at', None)
    for key in request_data:
        setattr(city, key, request_data[key])
    city.save()
    return jsonify(city.to_dict()), 200
