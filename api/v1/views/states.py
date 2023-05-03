#!/usr/bin/python3
"""View to handle API actions related to State objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_get(state_id=None):
    """Manipulate State object by state_id, or all objects if
    state_id is None
    """
    from models.state import State
    states = storage.all(State)

    # GET REQUESTS
    if request.method == 'GET':
        if not state_id:  # if no, state id specified, return all
            return jsonify([obj.to_dict() for obj in states.values()])

        key = 'State.' + state_id
        try:  # if obj exists in dictionary, convert from obj -> dict -> json
            return jsonify(states[key].to_dict())
        except KeyError:
            abort(404)  # if State of state_id does not exist

    # DELETE REQUESTS
    elif request.method == 'DELETE':
        try:
            key = 'State.' + state_id
            storage.delete(states[key])
            storage.save()
            return jsonify({}), 200
        except:
            abort(404)

    # POST REQUESTS
    elif request.method == 'POST':
        # convert JSON request to dict
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # instantiate, store, and return new State object
        if 'name' in body_request:
            new_state = State(**body_request)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        else:  # if request does not contain required attribute
            abort(400, 'Missing name')

    # PUT REQUESTS
    elif request.method == 'PUT':
        key = 'State.' + state_id
        try:
            state = states[key]

            # convert JSON request to dict
            if request.is_json:
                body_request = request.get_json()
            else:
                abort(400, 'Not a JSON')

            for key, val in body_request.items():
                if key != 'id' and key != 'created_at' and key != 'updated_at':
                    setattr(state, key, val)

            storage.save()
            return jsonify(state.to_dict()), 200

        except KeyError:
            abort(404)

    # UNSUPPORTED REQUESTS
    else:
        abort(501)
