#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
def all_states():
    if request.method == 'GET':
        return jsonify([i.to_dict() for i in storage.all(State).values()])
    if request.method == 'POST':
        if request.get_json():
            body = request.get_json()
        else:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in body:
            return make_request(jsonify({"error": "Missing name"}), 400)
        new_state = State(**body)
        new_state.save()
        if storage.get(State, new_state.id) is not None:
            return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<string:id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def D_G_P_state(id):
    """"get, delete and update an instance of state"""
    d = storage.get(State, id)
    if d is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(d.to_dict())
    if request.method == 'DELETE':
        storage.delete(d)
        storage.save()
        return jsonify({})
    if request.method == "PUT":
        if request.get_json():
            body = request.get_json()
        else:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        _e_k = ["id", "created_at", "updated_at"]
        for k, v in body.items():
            if k not in _e_k:
                setattr(d, k, v)
        d.save()
        return make_response(jsonify(d.to_dict()), 200)
