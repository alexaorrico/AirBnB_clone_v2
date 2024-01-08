#!/usr/bin/python3
"""
View for State objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.state import State
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_state_objects():
    """
    Retrieve a list of all State objects.

    Returns:
    - JSON representation of the list of State objects.

    Example:
    $ curl http://127.0.0.1:5000/api/v1/states
    Output: JSON representation of all State objects
    """
    all_objs = storage.all(State)
    return jsonify([obj.to_dict() for obj in all_objs.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_objects(state_id):
    """
    Retrieve a specific State object based on its ID.

    Parameters:
    - state_id: The ID of the State object to retrieve.

    Returns:
    - JSON representation of the specified State object.

    Example:
    $ curl http://127.0.0.1:5000/api/v1/states/1
    Output: JSON representation of the State object with ID 1
    """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_objects(state_id):
    """
    Delete a specific State object based on its ID.

    Parameters:
    - state_id: The ID of the State object to delete.

    Returns:
    - Empty JSON response with HTTP status code 200 upon successful deletion.

    Example:
    $ curl -X DELETE http://127.0.0.1:5000/api/v1/states/1
    Output: {}
    """
    obj = storage.get(State, state_id)
    if obj is None or not obj:
        abort(404)

    obj.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a new State object.

    Returns:
    - JSON representation of the newly created State object.
    - HTTP status code 201 upon successful creation.

    Example:
    $ curl -X POST -H "Content-Type: application/json" \
      -d '{"name": "New State"}' http://127.0.0.1:5000/api/v1/states
    Output: JSON representation of the newly created State object
    """

    data = request.get_json()

    if not data:
        abort(404, "Not a JSON")
    elif 'name' not in data.keys():
        abort(404, 'Missing name')

    obj = State(**data)
    storage.new(obj)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_objects(state_id):
    """
    Update a specific State object based on its ID.

    Parameters:
    - state_id: The ID of the State object to update.

    Returns:
    - JSON representation of the updated State object.
    - HTTP status code 200 upon successful update.

    Example:
    $ curl -X PUT -H "Content-Type: application/json" \
      -d '{"name": "Updated State"}' http://127.0.0.1:5000/api/v1/states/1
    Output: JSON representation of the updated State object
    """
    obj = storage.get(State, state_id)

    if obj is None or not obj:
        abort(404)

    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    storage.save()

    return make_response(jsonify(obj.to_dict()), 200)
