#!/usr/bin/python3
"""modify user objects via APIs"""
from models.user import User
from flask import jsonify, make_response, abort, request
from models import storage
from api.v1.views import app_views


def abortNotExists(cls, obj_id):
    """exit with a 404 status if obj not found"""
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_users(user_id=None):
    """retrieve a user object"""
    if not user_id:
        objs_dict = storage.all(User)
        obj_list = []
        for obj in objs_dict.values():
            obj_list.append(obj.to_dict())
        return make_response(jsonify(obj_list))

    else:
        obj = abortNotExists(User, user_id)
        return make_response(jsonify(obj.to_dict()))


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_users():
    """create a new user object"""
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    if "email" not in data.keys():
        abort(400, description="Missing email")
    if "password" not in data.keys():
        abort(400, description="Missing password")

    new_obj = User(**data)
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id):
    """Deletes a user object: DELETE /api/v1/users/<user_id>"""
    obj = abortNotExists(User, user_id)
    storage.delete(obj)
    storage.save()
    return make_response({}, 200)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def put_user(user_id):
    """Updates a user object: PUT /api/v1/users/<user_id>"""
    obj = abortNotExists(User, user_id)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, val in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj, key, val)

    storage.save()
    return make_response(obj.to_dict(), 200)
