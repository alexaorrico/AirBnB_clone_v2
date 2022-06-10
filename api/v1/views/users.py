#!/usr/bin/python3
""" User view """
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """
    Retrieves the list of all User objects
    ---
    tags:
      - User
    responses:
      200:
        description: List of all Users
        schema:
          type: array
          items:
            type: object
            properties:
              __class__:
                type: string
              created_at:
                type: string
              email:
                type: string
              first_name:
                type: string
              id:
                type: string
              last_name:
                type: string
              updated_at:
                type: string
          example:
            [
              {
                "__class__": "User",
                "created_at": "2022-05-31T20:42:53.350872",
                "email": "john@snow.com",
                "first_name": "Jon",
                "id": "9d475737-0548-4f49-a404-7b347d1f01de",
                "last_name": "Snow",
                "updated_at": "2022-05-31T20:42:53.350872"
              },
              {
                "__class__": "User",
                "created_at": "2022-05-31T20:42:53.350872",
                "email": "daenerys@hbtn.io",
                "first_name": "Daenerys",
                "id": "c1f4d071-c263-41eb-b06f-1dd7e66028c7",
                "last_name": "Targaryen",
                "updated_at": "2022-05-31T20:42:53.350872"
              }
            ]
    """
    users = storage.all(User)
    return jsonify([obj.to_dict() for obj in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """
    Retrieves a User object
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        required: true
    responses:
      200:
        description: User found
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            email:
              type: string
            first_name:
              type: string
            id:
              type: string
            last_name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "User"
            created_at: "2022-05-31T20:42:53.350872"
            email: "daenerys@hbtn.io"
            first_name: "Daenerys"
            id: "c1f4d071-c263-41eb-b06f-1dd7e66028c7"
            last_name: "Targaryen"
            updated_at: "2022-05-31T20:42:53.350872"
      404:
        description: No user found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        required: true
    responses:
      200:
        description: User deleted
        schema:
          type: object
      404:
        description: No user found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a new User
    ---
    tags:
      - User
    parameters:
      - name: create_user
        description: User's information to be stored
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
            first_name:
              type: string
            last_name:
              type: string
          example:
            email: "draka@tech.com"
            password: "draka666"
            first_name: "Draka"
            last_name:
    responses:
      201:
        description: User created
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            email:
              type: string
            first_name:
              type: string
            id:
              type: string
            last_name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "User"
            created_at: "2022-06-01T02:31:30.272867"
            email: "draka@tech.com"
            first_name: "Draka"
            id: "7fac35828-aecc-4760-80ce-efe65bb58487"
            last_name:
            updated_at: "2022-06-01T02:31:30.272867"
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not a JSON"
    """
    new_user = request.get_json()
    if new_user is None:
        abort(400, 'Not a JSON')
    if 'email' not in new_user:
        abort(400, 'Missing email')
    if 'password' not in new_user:
        abort(400, 'Missing password')
    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_id_put(user_id):
    """
    Updates a User object
    ---
    tags:
      - User
    parameters:
      - name: user_id
        in: path
        required: true
      - name: update_user
        description: User's information to be updated
        in: body
        required: true
        example:
          {
            "first_name": "Draka"
          }
    responses:
      200:
        description: User updated
        schema:
          type: object
          properties:
            __class__:
              type: string
            created_at:
              type: string
            email:
              type: string
            first_name:
              type: string
            id:
              type: string
            last_name:
              type: string
            updated_at:
              type: string
          example:
            __class__: "User"
            created_at: "2022-06-01T02:31:30.272867"
            email: "draka@tech.com"
            first_name: "Draka"
            id: "7fac35828-aecc-4760-80ce-efe65bb58487"
            last_name:
            updated_at: "2022-06-01T02:31:30.272867"
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not a JSON"
      404:
        description: No user found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")
    for key, value in request_json.items():
        if key != 'id' and key != 'email' and \
                key != 'created_at' and key != 'updated_at':
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
