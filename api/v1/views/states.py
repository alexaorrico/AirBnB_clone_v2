#!/usr/bin/python3
"""This module is in charge of handling requests for state-type objects."""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states')
def states():
    """This method is responsible for providing a list of all
        objects of type state as a json representation.

    Returns:
        dict: All State objects.

    """
    objs = [ob.to_dict() for ob in storage.all(State).values()]
    return jsonify(objs)


@app_views.route('/states/', methods=['POST'])
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states_id(state_id=None):
    """This method is in charge of handling all http requests
        referring to State class objects.

    Args:
        state_id (str, None): Id of State object. Defaults to None.

    Returns:
        dict: returns a specific value depending on the type of request.

    """
    obj = storage.get(State, state_id)
    # Get a specific State object through the HTTP GET request.
    if request.method == 'GET':
        if obj is not None:
            return obj.to_dict()
        abort(404)
    # Delete a specific State object through the HTTP DELETE request.
    elif request.method == 'DELETE':
        if obj is not None:
            storage.delete(obj)
            storage.save()
            return {}, 200
        abort(404)
    # Create a new State object through the HTTP POST request.
    elif request.method == 'POST':
        if request.get_json(silent=True):
            if "name" in request.get_json(silent=True):
                obj = State(**request.get_json())
                storage.new(obj)
                storage.save()
                return obj.to_dict(), 201
            return {"error": "Missing name"}, 400
        return {"error": "Not a JSON"}, 400
    # Update a specific State object through the HTTP PUT request.
    elif request.method == 'PUT':
        if obj is not None:
            if request.get_json(silent=True):
                fix_dict = request.get_json()
                attributes = ["id", "created_at", "updated_at"]
                for k, v in fix_dict.items():
                    if k not in attributes:
                        setattr(obj, k, v)
                obj.save()
                return obj.to_dict(), 200
            return {"error": "Not a JSON"}, 400
        abort(404)
