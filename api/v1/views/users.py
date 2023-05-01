#!/usr/bin/python3
"""restful API functions for User"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route("/users",
                 strict_slashes=False,
                 methods=["GET", "POST"]
                 )
@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=["DELETE", "PUT", "GET"])
def user_end_points(user_id=None):
    """to get users"""
    obj_users = storage.all(User)
    my_dict = [obj.to_dict() for obj in obj_users.values()]
    if not user_id:
        if request.method == "GET":
            return jsonify(my_dict)

        elif request.method == "POST":
            imput = request.get_json()
            if not imput:
                abort(400, "Not a JSON")
            elif not imput["email"]:
                abort(400, "Missing email")
            elif not imput["password"]:
                abort(400, "Missing password")
            else:
                new_user = User(**imput)
                new_user.save()
                return jsonify(new_user.to_dict()), 201
    else:
        if request.method == "GET":
            for user in my_dict:
                if user.get('id') == user_id:
                    return jsonify(user)
            abort(404)
        elif request.method == "DELETE":
            for ob in obj_users.values():
                if ob.id == user_id:
                    storage.delete(ob)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
        elif request.method == "PUT":
            new_dict = storage.get(User, user_id)
            get_new_name = request.get_json()
            if not get_new_name:
                abort(400, "Not a JSON")
            for user in obj_users.values():
                if user.id == user_id:
                    new_dict.__dict__.update(get_new_name)
                    new_dict.save()
                    return jsonify(new_dict.to_dict()), 200
            abort(404)
