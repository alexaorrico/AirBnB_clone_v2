#!/usr/bin/python3
"""States module """
from api.v1.views import app_views
from flask import jsonify, abort
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
