#!/usr/bin/python3
""" CRUD operation on city object"""
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import abort, request, make_response


@app_views.route('/states/<id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_by_state(id):
    """
    handling get method for all city in a state
    """
    state = storage.get(State, id)
    if state is None:
        abort(404)
    cities = []
    for i in state.cities:
        cities.append(i.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<id>', methods=['GET'], strict_slashes=False)
def city_get(id):
    """
    handling get method for a single city
    """
    city = storage.get(City, id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<id>', methods=['DELETE'], strict_slashes=False)
def city_delete(id):
    """
    handling delete method
    """
    city = storage.get(City, id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(id):
    """
    handling post method
    """
    state = storage.get(State, id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data or data['name'] == "":
        abort(400, "Missing name")
    data['state_id'] = id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('cities/<id>', methods=['PUT'], strict_slashes=False)
def city_put(id):
    """
    handling put for updating city object
    """
    city = storage.get(City, id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            city.bm_update(key, value)
    city.save()
    return jsonify(city.to_dict()), 200
