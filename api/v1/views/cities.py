#!/usr/bin/python3
"""cities api"""
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def cities(state_id):
    """get's all cities"""
    content = []
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    for city_data in states.cities:
        content.append(city_data.to_dict())
    return jsonify(content)


@app_views.route("/cities/<string:city_id>", methods=['GET'])
def cities_id(city_id):
    """cities with id"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_cities(city_id):
    """delete cities"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    storage.delete(cities)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def post_cities(state_id):
    """post cities"""
    validated_states = storage.get(State, state_id)
    if validated_states is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    print(data)
    city_instance = City(state_id=state_id, **data)
    city_instance.save()
    return jsonify(city_instance.to_dict()), 201


@app_views.route("/cities/<string:cities_id>", methods=['PUT'])
def update_cities(cities_id):
    """update cities"""
    cities = storage.get(City, cities_id)
    if cities is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json(force=True, silent=True)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(cities, key, value)
    cities.save()
    return jsonify(cities.to_dict()), 200
