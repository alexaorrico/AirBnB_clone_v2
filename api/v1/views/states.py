#!/usr/bin/python3
"""
    HBNB_V3: Task 7
"""
from api.v1.views.index import app_views, State
from models import storage
from flask import jsonify, request, abort, make_response


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def viewallthestatethings():
    """Retrieves the list of all State objects"""

    if request.method == 'GET':
        stl = storage.all(State)
        states = [state.to_dict() for state in stl.values()]
        return jsonify(states)
    if request.method == 'POST':
        try:
            body = request.get_json()
            if "name" not in body.keys():
                return "Missing name", 400
            else:
                newstate = State(**body)
                """for k in body.keys():
                    setattr(newstate, k, body.get(k))"""
                """newstate.__dict__.update(body)"""
                newstate.save()
                return jsonify(newstate.to_dict()), 201
        except:
            return "Not a JSON", 400


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def stateidtime(state_id):
    """Handles a state object with said id depending on HTTP request"""
    stl = storage.get(State, state_id)
    if stl is not None:
        sd = stl.to_dict()
        if request.method == 'GET':
            return jsonify(sd)
        if request.method == 'DELETE':
            storage.delete(stl)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            try:
                body = request.get_json()
                body.pop("id", "")
                body.pop("created_at", "")
                body.pop("updated_at", "")
                """s.__dict__.update(body)"""
                for k in body.keys():
                    setattr(stl, k, body.get(k))
                """s.save()"""
                stl.save()
                sd = stl.to_dict()
                return jsonify(sd)
            except:
                return "Not a JSON", 400

    else:
        abort(404)
