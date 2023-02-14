#!/usr/bin/python3
''' Routes for state objects '''
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_all_states():
    ''' get all state objs '''
    data = storage.all(State)
    new = [val.to_dict() for key, val in data.items()]
    return jsonify(new)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    ''' returns an individual state object '''
    obj = storage.get(State, state_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404, 'Not found')
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    ''' deletes an individual state '''
    obj = storage.get(State, state_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404, 'Not found')

    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    ''' updates an individual state '''
    obj = storage.get(State, state_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404, 'Not found')
    args = request.get_json()
    if not args:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in args.items():
        if k not in ["id", "updated_at", "created_at"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    ''' create a state if doesn't already exist '''
    args = request.get_json()
    if not args:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in args:
        return jsonify({"error": "Missing name"}), 400
    obj = State(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201

