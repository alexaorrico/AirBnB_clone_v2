#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import State, storage


@app_views.route('/api/v1/states',
                 methods=['GET', 'POST'], strict_slashes=False)
def states():
    if request.method == 'GET':

        return jsonify([value.to_dict()
                        for value in storage.all('State').values()])

    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400

        new_state = State(**post)
        new_state.save()
        return jsonify(new_state.dict()), 200


@app_views.route('/api/v1/states/<string:state_id>',
                 methods=['PUT', 'GET', 'DELETE'], strict_slashes=False)
def get_state_id(state_id):
    """Retrieves a state with the specified id"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(state.to_dict())

    elif request.method == 'DELETE':
        state = storage.get('State', state_id)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        item = request.get_json()
        if item is None or item != type(dict):
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in item.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
                storage.save()
        return jsonify(state.to_dict()), 200
