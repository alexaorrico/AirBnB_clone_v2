#!/usr/bin/python3
"""module state"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def user(id=None):
    """Show users"""
    list_user = []
    for user_objs in storage.all('User').values():
            list_user.append(user_objs.to_dict())
    return jsonify(list_user)


@app_views.route('/users/<id>', methods=['GET', 'DELETE', 'PUT'])
def user_delete(id=None):
    """Users delete function
    """
    obj_user = storage.get('User', id)
    if obj_user is None:
        abort(404)
    if request.method == 'DELETE':
        obj_user.delete()
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        do_put = request.get_json()
        if not do_put:
            abort(400, "Not a JSON")
        [setattr(obj_user, k, v) for k, v in do_put.items()
         if k not in ["id", "email", "created_at", "updated_at"]]
    obj_user.save()
    return jsonify(obj_user.to_dict()), 200


@app_views.route('/users', methods=['POST'])
def user_post():
    """Create User
    """
    if request.json:
        if "email" in request.json:
            if "password" in request.json:
                do_post = request.get_json()
                new_obj = User(**do_post)
                new_obj.save()
                return jsonify(new_obj.to_dict()), 201
            else:
                abort(400, "Missing password")
        else:
            abort(400, "Missing email")
    else:
        abort(400, "Not a JSON")
