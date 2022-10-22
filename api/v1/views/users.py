#!/usr/bin/python3
""" index module """


from api.v1.views import user_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.state import State


@user_views.route('users', strict_slashes=False)
def get_users():
    """ returns a list of all the users in db """
    users = storage.all(User)
    lst = [user.to_dict() for user in users.values()]
    return jsonify(lst)


@user_views.route('users/<user_id>', strict_slashes=False)
def get_user_with_id_eq_user_id(user_id):
    """ returns a user with id == user_id """
    user = storage.get(User, user_id)
    return jsonify(user.to_dict()) if user else abort(404)


@user_views.route('users/<user_id>', strict_slashes=False,
                  methods=["DELETE"])
def delete_user_with_id_eq_user_id(user_id):
    """ deletes a user with id == user_id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@user_views.route('users', strict_slashes=False,
                  methods=["POST"])
def create_user():
    """ creates a new user """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400
    email = data.get("email")
    passwd = data.get("password")

    if not email:
        return jsonify({
            "error": "Missing email"
            }), 400

    if not passwd:
        return jsonify({
            "error": "Missing password"
            }), 400

    user = User(**data)
    user.save()
    return jsonify(
        user.to_dict()
        ), 201


@user_views.route('users/<user_id>', strict_slashes=False,
                  methods=["PUT"])
def update_user_with_id_eq_user_id(user_id):
    """ updates a user's record """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400

    user_dict = user.to_dict()
    dont_update = ["id", "email", "created_at", "updated_at"]
    for skip in dont_update:
        data[skip] = user_dict[skip]
    user_dict.update(data)
    user.delete()
    storage.save()
    updated_user = User(**user_dict)
    updated_user.save()
    return jsonify(
            updated_user.to_dict()
            )


@user_views.route('states/<state_id>/users', strict_slashes=False)
def get_users_of_state(state_id):
    """ returns list of users associated with state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(
                [user.to_dict() for user in state.users]
            )


@user_views.route('states/<state_id>/users', strict_slashes=False,
                  methods=["POST"])
def create_linked_to_state_user(state_id):
    """ returns list of users associated with state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
                "error": "Not a JSON"
            }), 400
    name = data.get("name")
    if not name:
        return jsonify({
                "error": "Missing name"
            }), 400

    user = User(**data)
    # state.users.append(user)
    user.state_id = state.id
    user.save()
    state.save()
    return(
        jsonify(user.to_dict())
        ), 201
