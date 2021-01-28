#!/usr/bin/python3
"""users module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """
    Retrieves the list of all State objects or
    State objec from a rout
    """
    if user_id is None:
        st_all = []
        for st in storage.all(User).values():
            st_all.append(st.to_dict())
        return jsonify(st_all)
    elif storage.get(User, user_id):
        return jsonify(storage.get(User, user_id).to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """
    delete state if id is match with obj
    """
    if storage.get(User, user_id):
        storage.delete(storage.get(User, user_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def post_user():
    """
    arreglar
    """

    user_dict = request.get_json()

    if user_dict is None:
        abort("Not a JSON", 400)
    if "email" not in user_dict.keys():
        abort("Missing email", 400)
    if "password" not in user_dict.keys():
        abort("Missing password", 400)

    new_User = User(**user_dict)
    new_User.save()

    return jsonify(new_User.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """
    arreglar
    """

    data = request.get_json()

    obj = storage.get(User, user_id)

    if obj is None:
        abort(404)

    if data is None:
        return "Not a JSON", 400

    for k, v in data.items():
        if k in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(obj, k, v)
    storage.save()

    return jsonify(obj.to_dict()), 200
