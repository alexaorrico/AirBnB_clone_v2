#!/usr/bin/python3
'''Contains the states view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state():
    """Retrieves the list of all State objects"""
    all_sts = storage.all(State)
    return jsonify([st.to_dict() for ost in all_sts.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """Retrieves a State object"""
    one_st = storage.get(State, state_id)
    if not one_st:
        abort(404)
    return jsonify(one_st.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """Deletes a State object"""
    st_deleted = storage.get(State, state_id)
    if not obj:
        abort(404)
    st_deleted.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Returns the new State with the status code 201"""
    new_st = request.get_json()
    if not new_st:
        abort(400, "Not a JSON")
    if 'name' not in new_obj:
        abort(400, "Missing name")
    st = State(**new_st)
    storage.new(st)
    storage.save()
    return make_response(jsonify(st.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates a State object """
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(st, k, v)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
