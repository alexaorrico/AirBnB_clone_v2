#!/usr/bin/python3
""" New view for State that handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import json
from models import storage
from models.state import State


cls = 'State'


@app_views.route('/states/', methods=['GET', 'POST'])
@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """returns State object or collection"""
    if request.method == 'GET':
        states = []
        objs = storage.all(cls)
        for key, val in objs.items():
            obj_dict = val.to_dict()
            states.append(obj_dict)
        return jsonify(states)
    else:
        name = "name"
        json_data = request.get_json(silent=True)
        if json_data is None:
            abort(400, "Not a JSON")
        if name not in json_data.keys():
            abort(400, "Missing name")
        new_obj = State(**json_data)
        storage.new(new_obj)
        storage.save()
        new_obj_dict = new_obj.to_dict()
        return make_response(jsonify(new_obj_dict), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def stateid(state_id):
    """Retrieves a single object if present or rase 404"""
    if request.method == 'GET':
        obj = storage.get(cls, state_id)
        if obj is None:
            abort(404)
        obj_dict = obj.to_dict()
        return jsonify(obj_dict)
    elif request.method == 'PUT':
        obj = storage.get(cls, state_id)
        if obj is None:
            abort(404)
        json_data = request.get_json(silent=True)
        if json_data is None:
            abort(400, "Not a JSON")
        for key, val in json_data.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(obj, key, val)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        obj = storage.get(cls, state_id)
        if obj is None:
            abort(404)
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
