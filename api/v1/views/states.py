#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_all_states():
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


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    obj = storage.get(State, state_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404, 'Not found')

    obj.delete()
    storage.save()
    storage.close()
    return jsonify({})
