#!/usr/bin/python3


"""  TODO: Doc """


from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


users_dicts = storage.all(User)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """  TODO: Doc """
    array_of_objs = []
    for value in users_dicts.values():
        array_of_objs.append(value.to_dict())
    return jsonify(array_of_objs)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_ById(user_id):
    """  TODO: Doc """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404, description="User not found")
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(user_id):
    """  TODO: Doc """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404, description="State not found")
    try:
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500, description="Error while deleting")


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_state():
    """  TODO: Doc """
    if request.is_json:
        data = request.get_json()
        if 'email' not in data:
            abort(400, description="Missing email")
        elif 'password' not in data:
            abort(400, description="Missing password")
        else:
            user_obj = User(**data)  # unpack dict as key:valus
            user_obj.save()
            return jsonify(user_obj.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """  TODO: Doc """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404, description="user not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    bad_keys = ['id', 'created_at', 'email', 'updated_at']
    for key in data.keys():
        if key not in bad_keys:
            setattr(user_obj, key, data[key])
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
