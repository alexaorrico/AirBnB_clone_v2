#!/usr/bin/python3
""" State view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
    Retrieves the list of all State objects
    ---
    tags:
      - State
    responses:
      200:
        description: List of all State
        schema:
          type: array
          items:
            type: object
            properties:
              __class__:
                type: string
              created_at:
                type: string
              id:
                type: string
              name:
                type: string
              updated_at:
                type: string
          example:
            [
              {
                "__class__": "State",
                "created_at": "2022-05-31T20:42:53.350872",
                "id": "421a55f1-7d82-45d9-b54c-a76916479545",
                "name": "Alabama",
                "updated_at": "2022-05-31T20:42:53.350872"
              },
              {
                "__class__": "State",
                "created_at": "2022-05-31T20:42:53.350872",
                "id": "aa95665c-6295-4b5a-8d15-96686e9da62e",
                "name": "Florida",
                "updated_at": "2022-05-31T20:42:53.350872"
              }
            ]
    """
    states = storage.all(State)
    return jsonify([obj.to_dict() for obj in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """
    Retrieves a State object
    ---
    tags:
      - State
    parameters:
      - name: state_id
        in: path
        required: true
    responses:
      200:
        description: State found
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            id:
              type: string
            name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "State"
            created_at: "2022-05-31T20:42:53.350872"
            id: "d2398800-dd87-482b-be21-50a3063858ad"
            name: "Chernobyl"
            updated_at: "2022-05-31T20:42:53.350872"
      404:
        description: No state found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """
    Deletes a State object
    ---
    tags:
      - State
    parameters:
      - name: state_id
        in: path
        required: true
    responses:
      200:
        description: State deleted
        schema:
          type: object
      404:
        description: No state found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """
    Create a new state
    ---
    tags:
      - State
    parameters:
      - name: create_state
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
          example:
            name: "Chernobyl"
    responses:
      201:
        description: State created
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            id:
              type: string
            name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "State"
            created_at: "2022-05-31T20:42:53.350872"
            id: "6b240c6f-c6a5-4545-b611-60b8ecaa9a4c"
            name: "Chernobyl"
            updated_at: "2022-05-31T20:42:53.350872"
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not a JSON"
    """
    new_state = request.get_json()
    if new_state is None:
        abort(400, 'Not a JSON')
    if 'name' not in new_state:
        abort(400, 'Missing name')
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_id_put(state_id):
    """
    Updates a State object
    ---
    tags:
      - State
    parameters:
      - name: state_id
        in: path
        required: true
      - name: update_state
        description: State's information to be updated
        in: body
        required: true
        example:
          {
            "name": "Mississippi"
          }
    responses:
      200:
        description: State updated
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            id:
              type: string
            name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "State"
            created_at: "2022-05-31T20:42:53.350872"
            id: "0d9148c0-f394-412d-addc-1e5eb4f3e8db"
            name: "Mississippi"
            updated_at: "2022-05-31T20:42:53.350872"
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not a JSON"
      404:
        description: No state found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")
    for key, value in request_json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
