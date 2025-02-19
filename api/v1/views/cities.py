#!/usr/bin/python3
""" The City Object view
"""

from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """ Retrieves cities under a state from storage by state id
    """
    retrieved_cities = []
    state = storage.get(State, state_id)
    if state:
        for city in state.cities:
            retrieved_cities.append(city.to_dict())
        return jsonify(retrieved_cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city_by_id(city_id):
    """ Retrieves one city from storage based on the id
    """
    city_id = str(city_id)
    try:
        return jsonify(storage.get(City, city_id).to_dict()), 200
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """ Deletes the city from storage by its given id
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Adds a new city to storage
    """
    state = storage.get(State, state_id)
    if state:
        body = request.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        if 'name' not in body:
            abort(400, 'Missing name')
        new_city = City(**body)
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Modifies the attributes of a city if they are not dates or id
    """
    city = storage.get(City, city_id)
    if city:
        body = request.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        for key, value in body.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
