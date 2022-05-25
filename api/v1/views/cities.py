#!/usr/bin/python3
"""cities conf"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """method that returns all city objects of a state via given state id"""
    list_objs = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    objs = storage.all(City)
    for obj in objs.values():
        if obj.state_id == state_id:
            list_objs.append(obj.to_dict())
    return jsonify(list_objs)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """method that returns a city obj based on id or 404"""
    objs = storage.all(City)
    for obj in objs.values():
        if obj.id == city_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """method that deletes a city obj based on id or 404"""
    objs = storage.all(City)
    for obj in objs.values():
        if obj.id == city_id:
            obj.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """method that creates a new city for a state with given data"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    data['state_id'] = state_id
    if 'name' in data.keys():
        new_obj = City(**data)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    else:
        abort(400, "Missing name")
