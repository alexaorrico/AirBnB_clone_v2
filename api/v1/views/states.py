#!/usr/bin/python3
"""
File that configures the routes of state
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False)
@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id=None):
    """
    Route to get states
    """
    list_obj = []
    if not state_id:
        for val in storage.all("State").values():
            list_obj.append(val.to_dict())
        return jsonify(list_obj)
    state_obj = storage.get("State", state_id)
    if state_obj:
        return jsonify(state_obj.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """
    deletes a State object
    """
    state_obj = storage.get("State", state_id)
    if state_obj:
        storage.delete(state_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def post_state():
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if data:
        if "name" in data:
            obj = State(**data)
            obj.save()
            return (jsonify(obj.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/states", methods=["PUT"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id=None):
    obj = storage.get("State", state_id)
    if state_id and obj:
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if data:
            for key, value in data.items():
                if (key != "id" and key != "state_id" and key != "created_at"
                   and key != "updated_at"):
                    setattr(obj, key, value)

            obj.save()
            return (jsonify(obj.to_dict()))
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
