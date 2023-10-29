#!/usr/bin/python3
"""state JSON"""
from flask import abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from json import dumps


def json_ser(obj):
    json_obj = {}
    for key in obj:
        json_obj[key] = obj[key].to_dict()
    return (json_obj)


@app_views.route('/states', methods=["GET"])
def states_list():
    return make_response(
        dumps(list(json_ser(storage.all(State)).values())),
        200)


@app_views.route('/states/<state_id>', methods=["GET"])
def state_obj(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        return abort(404)
    return make_response(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        return abort(404)
    storage.delete(obj)
    storage.save()
    return make_response({}, 200)


@app_views.route('/states', methods=['POST'])
def state_post():
    try:
        data = request.get_json()
        if 'name' not in data:
            return abort(400, description='Missing name')
        new_state = State(**data)
        storage.new(new_state)
        storage.save()
        return make_response(new_state.to_dict(), 201)
    except Exception:
        return abort(400, description="Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    try:
        data = request.get_json()
        for key in data:
            if key in ['id', 'created_at', 'updated_at']:
                continue
            value = data[key]
            if hasattr(state, key):
                try:
                    value = type(getattr(state, key))(value)
                except ValueError:
                    pass
            setattr(state, key, value)
        storage.save()
        return make_response(state.to_dict(), 200)
    except Exception:
        return abort(400, description="Not a JSON")
