#!/usr/bin/python3
"""Create a new view for City objects that handles all default RestFul API"""


from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def states(state_id=None):
    """view for State objects that handles all default RestFul API actions"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    all_city = state.cities
    city_list = []
    for cit in all_city:
        city_list.append(cit.to_dict())
    return jsonify(city_list)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities(city_id=None):
    """Retrieves a City object"""
    cit = storage.get('City', city_id)
    if cit is None:
        abort(404)
    return jsonify(cit.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id=None):
    """Deletes a City object:: DELETE /api/v1/states/state_id"""
    cit = storage.get('City', city_id)
    if cit is None:
        abort(404)
    storage.delete(cit)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_create(state_id=None):
    """Creates new city"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    if 'name' not in res:
        abort(400, "Missing name")
    newCity = City(**res)
    storage.new(newCity)
    storage.save()
    return jsonify(newCity.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def cities_put(city_id=None):
    """updates a value from an instance"""
    cit = storage.get('City', city_id)
    res = request.get_json()

    if cit is None:
        abort(404)
    if res is None:
        abort(400, "Not a JSON")
    for k, v in res.items():
        if k != 'id' and k != 'created_at' and \
           k != 'updated_at' and k != 'state_id':
            setattr(cit, k, v)
    storage.save()
    return jsonify(cit.to_dict()), 200
