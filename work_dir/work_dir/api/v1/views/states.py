#!/usr/bin/python3
"""

Flask web server creation to handle api petition-requests

"""
from flask import jsonify, abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """
    Retrieves the list of all State objects
    """
    objects = storage.all("State")
    list_obj = []
    for obj in objects.values():
        list_obj.append(obj.to_dict())
    return jsonify(list_obj)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def some_state(state_id):
    """
    Retrieves a State object if id is linked to some State object
    """
    some_objs = storage.get(classes["State"], state_id)
    if some_objs is None:
        abort(404)
    some_objs = some_objs.to_dict()
    return jsonify(some_objs)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_state(state_id):
    """
    Deletes a State object if id is linked to some State object
    """
    some_objs = storage.get(classes["State"], state_id)
    if some_objs is None:
        abort(404)
    storage.delete(some_objs)
    storage.save()
    return jsonify({})


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def post_state():
    """
    Create a new State object
    """
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    if "name" in data_json:
        new_state = classes["State"](**data_json)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """
    Update a State object
    """
    obj = storage.get(classes["State"], state_id)
    if obj is None:
        abort(404)
    data_json = request.get_json(force=True, silent=True)
    if (type(data_json) is not dict):
        abort(400, "Not a JSON")
    for key, value in data_json.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
