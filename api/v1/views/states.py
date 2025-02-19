#!/usr/bin/python3
"""module state"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states')
def state(id=None):
    """Show states
    ---
    tags:
        - States
    responses:
      200:
        description: List of states
      404:
        description: Resource not found
     """
    list_state = []
    if id:
        state_objs = storage.get('State', id)
        if state_objs is None:
            abort(404)
        else:
            return jsonify(state_objs.to_dict())
    for state_objs in storage.all('State').values():
            list_state.append(state_objs.to_dict())
    return jsonify(list_state)


@app_views.route('/states/<id>', methods=['GET', 'DELETE', 'PUT'])
def state_delete(id=None):
    """States
    ---
    tags:
        - States
    parameters:
      - name: id
        in: path
        type: string
    responses:
      200:
        description: List of states
      404:
        description: Resource not found
      400:
        description: Not a JSON
     """
    obj_state = storage.get('State', id)
    if obj_state is None:
        abort(404)
    if request.method == 'DELETE':
        obj_state.delete()
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        do_put = request.get_json()
        if not do_put:
            abort(400, "Not a JSON")
        [setattr(obj_state, k, v) for k, v in do_put.items()
         if k not in ["id", "created_at", "updated_at"]]
    obj_state.save()
    return jsonify(obj_state.to_dict()), 200


@app_views.route('/states', methods=['POST'])
def state_post():
    """Create states
    ---
    tags:
        - States
    parameters:
        - name: name
          in: body
          type: dictionary
    responses:
      200:
        description: New state
      400:
        description: Not a JSON
      400:
        description: Missind name
     """
    if request.json:
        if "name" in request.json:
            do_post = request.get_json()
            new_obj = State(**do_post)
            new_obj.save()
            return jsonify(new_obj.to_dict()), 201
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")
