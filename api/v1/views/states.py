#!/usr/bin/python3
"""
-------------------
New view for States
-------------------
"""

from models.state import State
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views

methods = ["GET", "DELETE", "POST", "PUT"]
@app_views.route("/states", methods=methods)
@app_views.route("/states/<id>", methods=methods)
def states(id=None):
    """
    ----------------
    Route for states
    ----------------
    """
    states = storage.all(State)
    if request.method == "GET":
        if id:
            key = "State.{}".format(id)
            if key in states.keys():
                return jsonify(states[key].to_dict())
            else:
                abort(404)
        else:
            result = []
            for state in states.values():
                result.append(state.to_dict())
            return jsonify(result)
    elif request.method == "DELETE":
        if id:
            key = "State.{}".format(id)
            if key in states.keys():
                states[key].delete()
                # No sabemos si hay que guardar
                storage.save()
                return jsonify({}), 200, {'ContentType': 'application/json'}
        abort(404)
    elif request.method == "POST":
        try:
            data = request.get_json()
            if "name" not in data.keys():
                return jsonify("Missing name"), 400, {'ContentType':
                                                      'application/json'}
            else:
                new_state = State(**data)
                # No sabemos si hay que guardar
                new_state.save()
                return jsonify(new_state.to_dict()), 201, {'ContentType':
                                                           'application/json'}
        except Exception as err:
            return jsonify("Not a JSON"), 400, {'ContentType':
                                                'application/json'}
    elif request.method == "PUT":
        if id:
            key = "State.{}".format(id)
            if key not in states.keys():
                abort(404)
            else:
                try:
                    data = request.get_json()
                    state = states[key]
                    for attr, value in data.items():
                        if attr not in ["id", "created_at", "updated_at"]:
                            setattr(state, attr, value)
                    # No sabemos si hay que guardar
                    storage.save()
                    return jsonify(state.to_dict()), 201, {'ContentType':
                                                           'application/json'}
                except Exception as err:
                    return jsonify("Not a JSON"), 400, {'ContentType':
                                                        'application/json'}
