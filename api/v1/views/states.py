#!/usr/bin/python3
""" This module contains a blue print for a web app """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'])
@app_views.route('/states', methods=['GET', 'POST'])
def post_get_state_obj():
    """ This function contains two http method handler

        GET:
            return the all state objects
        POST:
            create a new state object
    """
    if request.method == 'GET':
        state_objects = storage.all(State)
        object_list = []
        for obj in state_objects.values():
            object_list.append(obj.to_dict())
        return jsonify(object_list)
    elif request.method == 'POST':
        try:
            state_dict = request.get_json()
        except Exception:
            abort(400, description="Not a JSON")
        if "name" not in state_dict:
            abort(400, description="Missing name")
        new_state = State(**state_dict)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def delete_put_get_state_obj(state_id):
    """ This function contains two http method handler

        GET:
            get the state object with the respective id
        DELETE:
            delete the state object with the respective id
        PUT:
            update the state object with the respective id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            state_dict = request.get_json()
            for key, value in state_dict.items():
                if key != "id" and key != "created_at" and key != "updated_at":
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
        except Exception:
            abort(400, description="Not a JSON")
