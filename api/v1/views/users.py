#!/usr/bin/python3
""" User script """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_or_add_user():
    users = storage.all("User").values()
    if request.methods == 'GET':
        return jsonify([obj.to_dict() for obj in storage.all("User").
                        values()]), 200
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


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_byid(user_id=None):
    """user function"""
    user_data = storage.get("User", user_id)
    if user_id is None:
        abort(400)
    else:
        if request.methods == 'GET':
            return jsonify(user_data.to_dict()), 200
        elif request.methods == 'DELETE':
            storage.delete(user_data)
            storage.save()
            return {}, 200
        elif request.methods == 'PUT':
            if request.get_json:
                data = request.get_json
                for k, v in data.items():
                    if k not in ['id', 'email', 'created_at', ' updated_at']:
                        setattr(user_data, k, v)
                user_data.save()
                return jsonify(user_data.to_dict()), 200
            else:
                abort(400, 'Not a JSON')
