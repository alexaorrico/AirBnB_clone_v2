#!/usr/bin/python3
""" Contains Funstion that Handles requests to the /states endpoints."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, state


@app_views.route("/states",
                 strict_slashes=False,
                 defaults={'state_id': None},
                 methods=['GET', 'POST'])
@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
def state_endpoint(state_id):
    """Handles all requests to state endpoint."""
    if request.method == "GET":
        if state_id is None:
            return [obj.to_dict() for obj in storage.all(state.State).values()]
        elif state_id is not None:
            st_obj = storage.get("State", state_id)
            if not st_obj:
                abort(404)
            return jsonify(st_obj.to_dict())
    elif request.method == "POST":
        try:
            post_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        if 'name' not in post_data:
            return make_response("Missing name", 400)
        new_state = state.State()
        new_state.name = post_data['name']
        new_state.save()
        return make_response(new_state.to_dict(), 201)
    elif request.method == "PUT":
        try:
            put_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        st_obj = storage.get("State", state_id)
        if not st_obj:
            abort(404)
        for key, value in put_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj, key, value)
        st_obj.save()
        return make_response(jsonify(st_obj.to_dict()), 200)
    elif request.method == "DELETE":
        state_obj = storage.get("State", state_id)
        if state_obj is None:
            abort(404)
        state_obj.delete()
        storage.save()
        return (jsonify({}))
