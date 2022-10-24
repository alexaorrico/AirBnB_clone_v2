#!/usr/bin/python3
<<<<<<< HEAD
'''contains state routes'''
from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'])
def states():
    '''retrieves all state objects'''
    states = storage.all(State)
    data = [state.to_dict() for state in states.values()]
    return jsonify(data)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_from_id(state_id):
    '''retrieves state using id'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''deletes a state'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    '''creates a new state'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    data = request.get_json()
    obj = State(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    '''modifies state object'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
=======
""" States """

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, state


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getallstate():
    """Gets all states"""
    req = []
    for i in storage.all("State").values():
        req.append(i.to_dict())

    return jsonify(req)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate(state_id=None):
    """Gets a state"""
    stat = storage.get("State", state_id)
    if stat is None:
        abort(404)
    else:
        return jsonify(stat.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletestate(state_id=None):
    """Deletes a state"""
    stat = storage.get("State", state_id)
    if stat is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createstate():
    """Create a state"""
    stat = request.get_json(silent=True)
    if stat is None:
        abort(400, "Not a JSON")
    elif "name" not in stat.keys():
        abort(400, "Missing name")
    else:
        new_stat = state.State(**s)
        storage.new(new_stat)
        storage.save()
        return jsonify(new_stat.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updatestate(state_id=None):
    """Update a state"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)

    stat = request.get_json(silent=True)
    if stat is None:
        abort(400, "Not a JSON")
    else:
        for x, y in stat.items():
            if x in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(obj, x, y)
        storage.save()
        req = obj.to_dict()
        return jsonify(req), 200
>>>>>>> c02c8bf79a11e249678224b436b61ec738225fff
