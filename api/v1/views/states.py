#!/usr/bin/python3
"""States module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states(state_id=None):
    """
    Retrieves the list of all State objects or
    State objec from a rout
    """
    if state_id is None:
        st_all = []
        for st in storage.all(State).values():
            st_all.append(st.to_dict())
        return jsonify(st_all)
    elif storage.get(State, state_id):
        return jsonify(storage.get(State, state_id).to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id=None):
    """
    delete state if id is match with obj
    """
    if storage.get(State, state_id):
        storage.delete(storage.get(State, state_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """
    Post states
    """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif "name" not in data.keys():
        abort(400, "Missing name")
    else:
        new_state = State(**state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id=None):
    """
    PUT states
    """
    data = request.get_json()

    obj = storage.get("State", state_id)

    if obj is None:
        abort(404)

    if data is None:
        return "Not a JSON", 400

    for k, v in data.items():
        if k in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(obj, k, v)
    storage.save()

    return jsonify(obj.to_dict()), 200
