#!/usr/bin/python3
""" Handle RESTful API request for states"""

from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/states',
                 methods=['GET'],
                 strict_slashes=False)
def all_states():
    """ GET ALL AMENITIES """
    objs = storage.all(State).values()
    list_obj = []
    for obj in objs:
        list_obj.append(obj.to_dict())

    return jsonify(list_obj)


@app_views.route('/states/<state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ Retrieves a specific State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_instance(state_id):
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states',
                 methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Creates a State: POST /api/v1/states"""

    if not request.get_json():
        abort(400, description="Not a JSON")
    else:
        data = request.get_json()

    if 'name' in data:
        new_state = State(**data)
        new_state.save()
    else:
        abort(400, description="Missing name")

    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """update a State: POST /api/v1/states"""
    print("0")
    if not request.get_json():
        print("1")
        abort(400, description="Not a JSON")

    obj = storage.get(State, state_id)

    if not obj:
        print("2")
        abort(404)

    print("3")
    data = request.get_json()

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            print("por aca")
            setattr(obj, key, value)
    obj.save()

    return make_response(jsonify(obj.to_dict()), 200)
