#!/usr/bin/python3
"""City API"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def get_state_cities(state_id):
    """Returns all cities objects in a state"""

    state = storage.get(State, state_id)
    if state is not None:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/cities/<string:city_id>", strict_slashes=False,
                 methods=['GET'])
def get_city(city_id):
    """Returns a city with a given id"""

    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route("/cities/<string:city_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Delete a city"""
    city = storage.get(City, city_id)
    if city is not None:
        city.delete()
        return jsonify({})
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """Create a city"""

    state = storage.get(State, state_id)
    if state is not None:
        if request.is_json:
            data = request.get_json()
            city_name = data.get('name', None)
            if city_name is None:
                return jsonify({'error': 'Missing name'}), 400
            city = City(name=city_name, state_id=state_id)
            city.save()
            return jsonify(city.to_dict()), 201
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404


@app_views.route("/cities/<string:city_id>", strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """Updates a city"""
    city = storage.get(City, city_id)
    if city is not None:
        if request.is_json:
            data = request.get_json()
            data = {k: v for k, v in data.items() if k != 'id' and
                    k != 'created_at' and k != 'updated_at'}
            for k, v in data.items():
                setattr(city, k, v)
            city.save()
            return jsonify(city.to_dict()), 200
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({'error': 'Not found'}), 404
