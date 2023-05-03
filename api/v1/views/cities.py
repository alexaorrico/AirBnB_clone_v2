#!/usr/bin/python3
"""
a new view for City objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State
    using the state id
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_json = []
    for city in cities:
        cities_json.append(city.to_dict())
    return jsonify(cities_json)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """Retrieves a City object
     by city id
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object by city id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City under a
    state using the state id
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    name = request.get_json().get('name')
    city = City(name=name, state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(city_obj, k, v)
    storage.save()
    return jsonify(city_obj.to_dict())
