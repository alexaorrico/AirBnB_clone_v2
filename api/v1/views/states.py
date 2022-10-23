#!/usr/bin/python3
"""return dict representation of object"""
from AirBnB_clone_v3.models import state
from models import storage
from api.v1.views import app_views
from models.base_model import BaseModel
from models.state import State
from flask import jsonify, abort, request, make_response


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get():
    """gets all state objects"""
    result =[]
    for i in storage.all("State").values():
        result.append(i.to_dict())
    return jsonify(result)

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def specific_stateObj(state_id):
    """ get the specific object from state """
    for i in storage.all("State").values():
        if i.id == state_id:
            return i.to_dict()
    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def state_specific_delete(state_id):
    """ delete the inputed object from state """
    thing = storage.all('State')
    muricanState = "State." + state_id
    state = thing.get(muricanState)
    if state is None:
        abort(404)
    else:
        state.delete()
        storage.save()
        return (jsonify({}), 200)

@app_views.route('/states', strict_slashes=False, methods=['POST'])
def postStates():
    """ creates a new state """
    thing = request.get_json(silent=True)
    if thing is None or not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    state = thing.get("name")
    if state is None or len(thing) == 0:
        return (jsonify({"error": "Missing name"}), 400)
    s = State()
    s.name = state
    s.save()
    return (jsonify(s.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_specific_put(state_id):
    """ update the specific object from state """
    instance = None
    if not request.json:
        return make_response("Not a JSON", 400)
    check = ["id", "created_at", "updated_at"]
    for i in storage.all("State").values():
        if i.id == state_id:
            instance = i
            for key, value in request.json.items():
                if key not in check:
                    setattr(i, key, value)
                    i.save()
    if not instance:
        abort(404)
    return instance.to_dict(), 200