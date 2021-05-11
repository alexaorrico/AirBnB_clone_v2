#!/usr/bin/python3
'''Creates routes that handles states with JSON'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def state_lists():
    '''returns list of states or creates new one'''
    if request.method == 'POST':
        try:
            content = request.get_json()
            if content is None:
                abort(400, 'Not a JSON')
        except Exception as e:
            abort(400, 'Not a JSON')
        if 'name' not in content.keys():
            abort(400, 'Missing name')
        new_instance = State(name=content['name'])
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201
    else:
        state_list = []
        for state_obj in storage.all("State").values():
            state_list.append(state_obj.to_dict())
        return jsonify(state_list)


@app_views.route('/states/<id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def states_specific(id):
    '''manages specific state object'''
    state_target = storage.get(State, id)
    if state_target is None:
        abort(404)
    if request.method == 'PUT':
        try:
            content = request.get_json()
            if content is None:
                abort(400, 'Not a JSON')
        except Exception as e:
            abort(400, 'Not a JSON')
        ignore = ['id', 'created_at', 'updated_at']
        for key, val in content.items():
            if key not in ignore:
                setattr(state_target, key, val)
        state_target.save()
        return jsonify(state_target.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state_target)
        storage.save()
        return jsonify({})
    else:
        return jsonify(state_target.to_dict())
