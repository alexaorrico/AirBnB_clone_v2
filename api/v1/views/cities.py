#!/usr/bin/python3
'''city view for API'''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    '''list all city object of a given state'''
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404, 'Not found')
    if state_id:
        objs = storage.all('City').values()
        obj_list = []
        for obj in objs:
            if (state_id == obj.state_id):
                obj_list.append(obj.to_dict())
        return jsonify(obj_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def single_city(city_id):
    '''Retrieve city object'''
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    '''delete city object'''
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    '''return new city'''
    new_obj = request.get_json()
    if not new_obj:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if not State:
        abort(404)
    if 'name' not in new_obj:
        abort(400, "Missing name")
    obj = State(**new_obj)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    '''update city object'''
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
