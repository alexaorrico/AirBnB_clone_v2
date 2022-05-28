#!/usr/bin/python3
"""
-------------------
New view for States
-------------------
"""

from models.state import State
from models import storage
from flask import jsonify, request, abort, Response
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
                return jsonify({}), 200, {'ContentType':'application/json'}
                #return jsonify({}), 200
                #return Response("{'a':'b'}", status=200, mimetype='application/json')
        abort(404)
    elif request.method == "POST":
        try:
            data = request.get_json()
            if "name" not in data.keys():
                # abort(400)
                return jsonify("Missing name"), 400, {'ContentType':'application/json'}
            else:
                new_state = State(**data)
                #new_state.save()
                return jsonify(new_state.to_dict()), 201, {'ContentType':'application/json'}
        except Exception as err:
            # abort(400)
            return jsonify("Not a JSON"), 400, {'ContentType':'application/json'}
    elif request.method == "PUT":
        if id:
            key = "State.{}".format(id)
            if key not in states.keys():
                abort(404)
                return
            else:
                try:
                    data = request.get_json()
                    state = states[key]
                    for attr, value in data.items():
                        setattr(state, attr, value)
                    #new_state.save()
                    return jsonify(state.to_dict()), 201, {'ContentType':'application/json'}
                except Exception as err:
                    # abort(400)
                    return jsonify("Not a JSON"), 400, {'ContentType':'application/json'}
                    
                return jsonify(states[key].to_dict()) 
