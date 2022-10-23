#!/usr/bin/python3
"""cities route"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """Endpoint to retreive cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    all_city = []
    cities = storage.all(City)
    for city in state.cities:
        all_city.append(city.to_dict())
    return jsonify(all_city)


@app_views.route('/cities/<string:city_id>',
                 strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """retreieves a city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """deletes a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def post_city(state_id):
    """creates a new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    data = request.get_json()
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<string:city_id>',
                 strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """updates a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at', 'state_id']
    for k, v in data.items():
        if k not in ignore:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
