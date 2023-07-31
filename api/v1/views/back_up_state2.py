#!/usr/bin/python3
"""Retrieving State objects"""

from models.state import State
from flask import request, jsonify, abort
from models import storage
from api.v1.views import app_views

states = storage.all(State).values()
state_list = []
for state in states:
    state_list.append(state.to_dict())


@app_views.route('/states', methods=["GET", "POST"], strict_slashes=False)
def get_states():
    """A function to perform GET and POST request on http"""
    if request.method == 'GET':
        return jsonify(state_list)

    elif request.method == 'POST':
        name = request.get_json()
        if name.get('name') is None:
            abort(400, 'Missing name')
        try:
            value = name['name']
            new_dict = {
                '__class__': State.__name__,
                'created_at': State().created_at,
                'name': value,
                'id': State().id,
                'updated_at': State().updated_at
            }
            return new_dict, 201

        except Exception as e:
            abort(400, "Not a JSON")


@app_views.route('/states/<state_id>',
                 methods=['GET', "DELETE", "PUT"], strict_slashes=False)
def get_delete_put(state_id):
    """A function to perform http GET, DELETE and PUT method"""
    check = 0
    if request.method == 'GET':
        for i in state_list:
            if i['id'] == state_id:
                return i
                check = 1
                break
        if check == 0:
            abort(404)

    elif request.method == "DELETE":
        for i in state_list:
            if i['id'] == state_id:
                check = 1
                return "{}", 200
                break
        if check == 0:
            abort(404)

    elif request.method == "PUT":
        for i in state_list:
            if i['id'] == state_id:
                try:
                    data = request.get_json()
                    new_data = {}
                    for key in data:
                        if key == 'id' or key == 'created_at'\
                                or key == 'updated_at':
                            continue
                        new_data[key] = data[key]
                    i.update(new_data)
                    return i, 200
                except Exception as e:
                    abort(400, "Not a JSON")
        if check == 0:
            abort(404)
