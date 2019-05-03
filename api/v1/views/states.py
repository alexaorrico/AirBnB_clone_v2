#!/usr/bin/python3
"""HolbertonBnB State view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
@swag_from("../apidocs/states/get_states.yml", methods=["GET"])
@swag_from("../apidocs/states/post.yml", methods=["POST"])
def states():
    """Defines GET and POST methods for the states route.

    GET - Retrives a list of all State objects.
    POST - Creates a State.
    """
    # GET method
    if request.method == "GET":
        return jsonify([s.to_dict() for s in storage.all("State").values()])

    # POST method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("name") is None:
        return "Missing name", 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
@swag_from("../apidocs/states/get_state_id.yml", methods=["GET"])
@swag_from("../apidocs/states/delete.yml", methods=["DELETE"])
@swag_from("../apidocs/states/put.yml", methods=["PUT"])
def state_id(state_id):
    """Defines GET, DELETE and PUT methods for a specific ID on states.

    GET - Retrieves a State object with the given id.
    DELETE - Deletes the State object with the given id.
    PUT - Updates the State object with a given JSON object of key/value pairs.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify(state.to_dict())

    # DELETE method
    elif request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({})

    # PUT method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "created_at", "updated_at"}
    [setattr(state, k, v) for k, v in data.items() if k not in avoid]
    state.save()
    return jsonify(state.to_dict())
