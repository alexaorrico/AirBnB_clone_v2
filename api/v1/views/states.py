#!/usr/bin/python3
from models.base_model import *
from flask import *
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False,
                 defaults={'state_id': None})
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False,)
def get_states(state_id):
    """Retrieves state object"""
    if state_id is None:
        list_obj = []
        for i in storage.all('State').values():
            list_obj.append(i.to_dict())
        return jsonify(list_obj)
    save = save = storage.get(State, state_id)
    if not save:
        error = make_response(jsonify({"error": "Not found"}), 404)
        return error.to_dict()
    save = save.to_dict()
    return (save)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """POST /api/v1/states"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    s = State(**data)
    s.save()
    return make_response(jsonify(s.to_dict()), 201)
