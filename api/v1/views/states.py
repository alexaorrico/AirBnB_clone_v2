#!/usr/bin/python3
""" handles all default RESTFul API actions"""

from models import storage
from models.state import State
from flask import jsonify, abort, request


@app.route('/states', method=['GET'], strict_slashes=False)
def list_all():
    """lists all state objects with GET method"""
    stats = storage.all(State).values()
    display = [obj.to_dict() for obj in stats]
    return (jsonify(display))


@app.route('/states/state_id', method=['GET'], strict_slashes=False)
def list_id(state_id):
    """lists state id with GET method"""
    retrieve_id = storage.get(State, state_id)
    if (retrieve_id is None):
        abort(404)
    display = retrieve_id.to_dict()
    return jsonify(display)


@app.route('/states/state_id', method=['DELETE'])
def delete_state(state_id):
    """deletes state id"""
    delete_id = storage.get(State, state_id)
    if delete_id is None:
        abort(404)
    else:
        storage.delete(delete_id)
        storage.save()
        return (jsonify({}), 200)


@app.route('/states', method=['POST'], strict_slashes=False)
def post_state():
    """Posts a new state"""
    posts = request.get_json()
    if posts is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in posts:
        return (jsonify({'error': 'Missing name'}), 400)
    posts_obj = State(**posts)
    posts_obj.save()
    return jsonify(posts_obj.to_dict()), 201


@app.route('/states/state_id', methods=['PUT'], strict_slashes=False)
def put_state_id(state_id):
    """Update State"""
    update = request.get_json()
    if update is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        keys = ['id', 'created_at', 'updated_at']
        for key, value in update.items():
            if key not in keys:
                setattr(state, key, value)
            else:
                pass
        state.save()
        return (jsonify(state.to_dict()), 200)
