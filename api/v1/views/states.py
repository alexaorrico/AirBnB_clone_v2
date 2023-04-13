#!/usr/bin/python3
""" state api module created """


from models.state import State
from flask import jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET', 'POST'], defaults={'id': None})
@app_views.route('/states/<id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def state_view(id=None):
    """ state view """
    if id is not None:
        my_states = storage.all(State)
        key = '{}.{}'.format(State.__name__, id)
        if key not in my_states.keys():
            return jsonify(error='Not found'), 404
        state = my_states[key]
        if request.method == 'GET':
            return jsonify(state.to_dict())
        elif request.method == 'DELETE':
            storage.delete(state)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            update_values = request.get_json()
            if type(update_values) is not dict:
                return jsonify(error='Not a JSON'), 400
            for key, val in update_values.items():
                ls = ['id', 'created_at', 'updated_at']
                if key not in ls:
                    setattr(state, key, val)
                storage.save()
                return jsonify(state.to_dict())
    else:
        if request.method == 'GET':
            my_states = storage.all(State)
            json_states = []
            for state in my_states.values():
                json_states.append(state.to_dict())
            response = jsonify(json_states)
            response.headers['Access-Control-Allow-Origin'] = '0.0.0.0'
            return response
        elif request.method == 'POST':
            update_values = request.get_json()
            if type(update_values) is not dict:
                return jsonify(error='Not a JSON'), 400
            if 'name' not in update_values.keys():
                return jsonify(error='Missing name'), 400
            x = State(name=update_values['name'])
            return jsonify(x.to_dict()), 201
