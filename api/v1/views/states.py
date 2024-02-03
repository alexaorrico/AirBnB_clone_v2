#!/usr/bin/python3
'''routes'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''returns json to the route'''
    obj = [obj.to_dict() for obj in storage.all('State').values()]
    return jsonify(obj)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    '''return by id'''
    obj = [obj.to_dict() for obj in storage.all('State').values()]
    for j in obj:
        if j['id'] == state_id:
            return j
    abort(404)
