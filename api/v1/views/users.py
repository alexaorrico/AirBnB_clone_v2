#!/usr/bin/python3
"""
This is module users
"""
from api.v1.views import (app_views, User, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_user(user_id=None):
    """Example endpoint returning a list of all users or of one specified
    Retrieves a list of all users or of one specified by user_id
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        enum: ["all", "32c11d3d-99a1-4406-ab41-7b6ccb7dd760"]
        required: true
        default: None

    definitions:

      User:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          email:
            type: string
          first_name:
            type: string
          last_name:
            type: string
          id:
            type: string
            description: the id of the user
          updated_at:
            type: string
            description: The date the object was updated
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of dictionarys or dictionary, each dict is a user
        schema:
          $ref: '#/definitions/User'
        examples:
            [{"__class__": "User",
              "_password": "pwd18",
              "created_at": "2017-03-25T02:17:06",
              "email": "noemail18@gmail.com",
              "first_name": "Susan",
              "id": "32c11d3d-99a1-4406-ab41-7b6ccb7dd760",
              "last_name": "Finney",
              "updated_at": "2017-03-25T02:17:06"}]
    """
    if user_id is None:
        all_users = [state.to_json() for state
                     in storage.all("User").values()]
        return jsonify(all_users)
    s = storage.get("User", user_id)
    if s is None:
        abort(404)
    return jsonify(s.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """Example endpoint deleting one user
    Deletes a user based on the user_id
    ---
    definitions:
      User:
        type: object
      Color:
        type: string
      items:
        $ref: '#/definitions/Color'

    responses:
      200:
        description: An empty dictionary
        schema:
          $ref: '#/definitions/User'
        examples:
            {}
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Example endpoint creates a user
    Creates a user based on the JSON body
    ---
    definitions:

      User:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          email:
            type: string
          first_name:
            type: string
          last_name:
            type: string
          id:
            type: string
            description: the id of the user
          updated_at:
            type: string
            description: The date the object was updated
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: A list of a dictionary, each dict is a user
        schema:
          $ref: '#/definitions/User'
        examples:
            [{"__class__": "User",
              "_password": "pwd18",
              "created_at": "2017-03-25T02:17:06",
              "email": "noemail18@gmail.com",
              "first_name": "Susan",
              "id": "32c11d3d-99a1-4406-ab41-7b6ccb7dd760",
              "last_name": "Finney",
              "updated_at": "2017-03-25T02:17:06"}]
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'email' not in r.keys():
        return "Missing email", 400
    if 'password' not in r.keys():
        return "Missing password", 400
    s = User(**r)
    s.save()
    return jsonify(s.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """Example endpoint updates a user
    Updates a user based on the JSON body
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        enum: ["32c11d3d-99a1-4406-ab41-7b6ccb7dd760"]
        required: true
        default: "32c11d3d-99a1-4406-ab41-7b6ccb7dd760"

    definitions:

      User:
        type: object
        properties:
          __class__:
            type: string
            description: The string of class object
          created_at:
            type: string
            description: The date the object created
          email:
            type: string
          first_name:
            type: string
          last_name:
            type: string
          id:
            type: string
            description: the id of the user
          updated_at:
            type: string
            description: The date the object was updated
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of a dictionary, each dict is a user
        schema:
          $ref: '#/definitions/User'
        examples:
            [{"__class__": "User",
              "_password": "pwd18",
              "created_at": "2017-03-25T02:17:06",
              "email": "noemail18@gmail.com",
              "first_name": "Susan",
              "id": "32c11d3d-99a1-4406-ab41-7b6ccb7dd760",
              "last_name": "Finney",
              "updated_at": "2017-03-25T02:17:06"}]
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    a = storage.get("User", user_id)
    if a is None:
        abort(404)
    for k in ("id", "email", "created_at", "updated_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(a, k, v)
    a.save()
    return jsonify(a.to_json()), 200
