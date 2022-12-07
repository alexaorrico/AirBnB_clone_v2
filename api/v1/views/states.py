#!/usr/bin/python3
from flask import flask, jsonify, request, abort
from models import storage 
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=["GET", "POST"]) # deberia sacarle el api/v1? ya estaria en el blueprint
def retrive_states():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        all_states = []

        for obj in storage.all("State").values():
            all_states.append(obj.to_dict())

        return jsonify(all_states)

    elif request.method == 'POST':
        http_data = request.get_json()
        if not http_data:
            abort(404, 'Not a JSON')
        if "name" not in http_data:
            abort(400, 'Missing name')
        
        new_state = State(**http_data)
        new_state.save()
        return new_state, 201


@app_views.route('/states/<state_id>', methods=["GET", "DELETE", "PUT"]) # deberia sacarle el api/v1? ya estaria en el blueprint
def state_by_id(state_id):
    """Retrieves, deletes or updates a State object by state_id"""
    if request.method == 'GET':
        if state_id is not None:
            for obj in storage.all("State").values():
                if obj.id == state_id:
                    return jsonify(obj.to_dict())

    elif request.method == 'DELETE':
        if state_id is not None:
            for obj in storage.all("State").values():
                if obj.id == state_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200

    elif request.method == 'PUT':
        if state_id is not None:
            for obj in storage.all("State").values():
                if obj.id == state_id:
                    http_data = request.get_json()
                    if not http_data:
                        abort(400, 'Not a JSON')

                    statics_attrs = ["id", "created_at", "updated_at"]
                    for key, value in http_data.items():
                        if key not in statics_attrs:
                            setattr(obj, key, value)
                    storage.save()
                    return jsonify(obj.to_dict()), 200                  
    else:
        abort(404)
