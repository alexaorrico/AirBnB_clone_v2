#!/usr/bin/python3
"""restful actions for users"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route('/api/v1/users', methods=["GET"],
                 strict_slashes=False)
def get_all_users():
    """gets all users"""
    user_list = []
    for user in storage.all(User).values:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/api/v1/users/<user_id>', methods=["GET"],
                 strict_slashes=False)
def get_user(id):
    """retrieves a user by id"""
    get_user = storage.get(User, id)
    if get_user is None:
        abort(404)
    else:
        return jsonify(get_user.to_dict())


@app_views.route('/api/v1/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def del_user(id):
    """deletes a user by id"""
    empty_dict = {}
    get_user = storage.get(User, id)
    if get_user is None:
        abort(404)
    else:
        storage.delete(get_user)
        storage.save()
        return empty_dict, 200


@app_views.route('/api/v1/users', methods["POST"],
                 strict_slashes=False)
def create_user(id):
    """creates a city object from state id"""
    user_json = request.get()
    get_user = storage.get(User, id)
    if get_user is None:
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    elif 'email' not in user_json:
        abort(400, description="Missing email")
    elif 'password' not in user_json:
        abort(400, description="Missing password")
    else:

        ###########################################
        ###########################################
        # how to actually create new user object? #
        ###########################################
        ###########################################
        return 201


@app_view.route('/api/v1/users/<user_id>', methods=["PUT"],
                strict_slashes=False)
def update_user(id):
    """updates a city object"""
    user_json = request.get_json
    get_user = storage.get(City, id)
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    if get_city is None:
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    else:
        for key, value in city_json.items:
            if key not in ignored_keys:
                setattr(get_user, key, value)
            storage.save()
        return jsonify(get_user.to_dict()), 200
