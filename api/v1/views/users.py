#!/usr/bin/python3
"""
New view for State objects that handles taht handles all default ResFul API.
"""


from flask import abort
from flask import jsonify
from models.user import User
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """
    """
    user_list = []
    for user in storage.all('User').values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """
    Return id of the function
    """
    userArr = storage.get("User", user_id)
    if userArr is None:
        abort(404)
    return jsonify(userArr.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def get_user_delete(user_id):
    """
    method Delete of the function
    """
    userArr = storage.get('User', user_id)
    if userArr is None:
        print("entre al ifffffffffffffffffffffffff")
        abort(404)
    else:
        print("entre al elseeeeeeeeeeeeeeeeeeeeeee")
        storage.delete(userArr)
        storage.save()
    return jsonify({}), 200



@app_views.route("/users", methods=['POST'], strict_slashes=False)
def set_user_POST():
    """
    User object
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    user_post = User(email=request.json["email"],
                     password=request.json["password"])
    storage.new(user_post)
    user_post.save()
    return jsonify(user_post.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def set_user_PUT(user_id):
    """
    method PUT
    """
    user = storage.get("User", user_id)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if user is None:
        abort(404)
    for atriv, val in request.get_json().items():
        if ((atriv != "id" and atriv != "state_id" and
             atriv != "created_at" and atriv != "updated_at")):
            setattr(user, atriv, val)
    storage.save()
    return jsonify(user.to_dict()), 200


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
