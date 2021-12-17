#!/usr/bin/python3
"""Creating user api app"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User

@app_views.route('/users/', methods=['GET', 'POST'], strict_slashes=False)
def allUsers():
    """retrieves a list of all users in db"""
    if request.method == "GET":
        all_users = []
        for key in storage.all(User).values():
            all_users.append(key.todict())
        return jsonify(all_users)
    
    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400
        
        all_users = User(**request.get_json().to_dict())
        if "password" not in all_users:
            return "Missing password", 400
        
        if "email" not in all_users:
            return "Missing email", 400

        storage.new(all_users)
        storage.save()
        return jsonify(all_users), 201

@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def user_id(user_id)
    """updates user_id"""
    if request.method == 'GET':
        user_data = storage.get(User, user_id)
        if user_data is not None:
            return jsonify(user_data.to_dict())
        abort(404)

    if request.method == "PUT":
        user_data = storage.get(User, user_id)
        if user_data is not None:
            if not request.is_json:
                return "Not a JSON", 400
            for key, value in request.get_json().items():
                setattr(user_data, key, value)
            storage.save()
            return jsonify(user_data.to_dict()), 200
        abort(404)
    
    if request.method == "DELETE":
        user_data = storage.get(User, user_id)
        if user_data is not None:
            storage.delete(user_data)
            storage.save()
            return jsonify({}), 200
        abort(404)