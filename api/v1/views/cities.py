#!/usr/bin/python3

"""
Create a new view for City objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get(state_id):
    """ Returns all objects """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    cList = []
    for c in cities:
        cList.append(c.to_dict())
    return jsonify(cList)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieve a city object by id"""
    obj = storage.get(City, city_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete an object by id"""
    obj = storage.get(City, city_id)
    if obj:
        obj.delete()
        storage.save()
        storage.reload()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create(state_id):
    """Create an object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if body.get('name') is None:
        abort(400, "Missing name")

    name = body.get('name')
    obj = City(name=name, state_id=state_id)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates an object"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
