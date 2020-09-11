#!/usr/bin/python3
"""
view for User objects that handles all default RestFul API action
"""

from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.user import User


# the followings are the entendpoints of the app_view blueprint
# in other words /status == /api/v1/status and /stats == /api/v1/stats
# we create that blueprint to access to all the endpoints easily

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """
    function to return the all State objects
    """
    all_users = []
    for user in storage.all('User').values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    function to return State object by id throught a GET method
    """
    all_users = storage.all("User").values()
    for user in all_users:
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    function to delete State object by id throught a DELETE method
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """
    function to create a new State object throught a POST method
    """
    dic_json = request.get_json()
    if not dic_json:
        return make_response("Not a JSON", 400)
    if "email" not in dic_json:
        return make_response("Missing email", 400)
    if "password" not in dic_json:
        return make_response("Missing password", 400)
    new_user = User(**dic_json)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    function to update a State object by id throught a PUT method
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    dic_json = request.get_json()
    if not dic_json:
        return make_response("Not a JSON", 400)
    for key, value in dic_json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)


if __name__ == "__main__":
    pass
