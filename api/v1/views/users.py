#!/usr/bin/python3
""" User script """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage

@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_or_add_user():
    users = storage.all(User).values()
    if request.methods == 'GET':
        return jsonify(users.to_dict())
    elif request.methods == 'POST':
        if request.get_json:
            data = request.get_json
            email = data.get("email")
            password = data.get('password')

            if email:
                abort(400, 'Missing email')
            if password:
                abort(400, 'Missing password')

            new_user = User(**data)
            storage.save(new_user)
            return jsonify(new_user.to_dict()), 201
        else:
            abort(400, 'Not a JSON')