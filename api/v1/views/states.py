#!/usr/bin/python3
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def state_list():
    '''Interested in list of all states'''
    if request.method == 'GET':
        state_list = storage.all('State')
        list_dict = [state.to_dict() for state in state_list.values()]
        return jsonify(list_dict)
    if request.method == 'POST':
        try:
            json_body = request.get_json()
            if not json_body:
                abort(400, 'Not a JSON')
            if not 'name' in json_body:
                abort(400, 'Missing name')
            state = State(**json_body)
            new_inst = storage.new(state)
            storage.save()
            return jsonify(state.to_dict()), 201
        except Exception as err:
            abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def state_detail(state_id):
    '''Interested in details of a specific state'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        try:
            json_body = request.get_json()
            if not json_body:
                abort(400, 'Not a JSON')
            for k, v in json_body.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(state, k, v)
            storage.save()
            return jsonify(state.to_dict())
        except Exception as err:
            abort(404)
