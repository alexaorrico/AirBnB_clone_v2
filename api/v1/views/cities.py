#!/usr/bin/python3
""" a view for city """
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_city(state_id):
    """retrieve all city"""
    citi = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        citi.append(city.to_dict())
    return jsonify(citi)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """deletes an instance of city using the given id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a city """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """updates a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_id', 'updates_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
