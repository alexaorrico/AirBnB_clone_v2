#!/usr/bin/python3
"""States views"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def view_users():
    """Returns the list of all User objects"""
    if request.method == 'POST':
        # Get the attributes from the request
        data = request.get_json()

        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        if 'id' in data.keys():
            data.pop("id")
        if 'created_at' in data.keys():
            data.pop("created_at")
        if 'updated_at' in data.keys():
            data.pop("updated_at")

        if 'email' not in data.keys():
            return jsonify({'error': 'Missing email'}), 400
        if 'password' not in data.keys():
            return jsonify({'error': 'Missing password'}), 400

        # Create the object
        obj = User(**data)

        # Save the object in storage
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201

    if request.method == 'GET':
        users = storage.all("User")
        list = []
        for name, user in users.items():
            list.append(user.to_dict())
        return jsonify(list)


@app_views.route('/users/<id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def view_user_id(id):
    """Returns a list of all User objects, or delete an
    object if a given id
    """
    user = storage.get(User, id)

    if user is None:
        return abort(404)

    if request.method == 'GET':

        return jsonify(user.to_dict())

    if request.method == 'DELETE':

        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, value)
        # This save is possibly not working to obtain
        # permanent changes in the data base
        storage.save()
        return jsonify(user.to_dict())
