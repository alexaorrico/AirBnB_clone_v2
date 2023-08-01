#!/usr/bin/python3
"""create get, delete, post, put methods for user instance"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def show_usr(user_id=None):
    """ This method shows all the users or one user based on id
    """
    if user_id is None:
        return jsonify([o.to_dict() for o in storage.all("User").values()])
    else:
        usr = storage.get("User", user_id)
        if usr:
            return jsonify(usr.to_dict())
        else:
            abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_usr(user_id):
    """This method deletes a userId
    """
    usr = storage.get("User", user_id)
    if usr:
        storage.delete(usr)
        storage.save()
        return (jsonify("{}"), 200)
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_usr():
    """This method creates a new user
    """
    vals = request.get_json(silent=True)
    u = User()
    if vals is None:
        abort(400, "Not a JSON")
    if "email" not in vals:
        abort(400, "Missing email")
    if "password" not in vals:
        abort(400, "Missing password")
    for k, v in vals.items():
        setattr(u, k, v)
    storage.new(u)
    storage.save()
    return (jsonify(u.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_usr(user_id):
    """This method updates the user
    """
    usr = storage.get("User", user_id)
    vals = request.get_json(silent=True)
    if vals is None:
        abort(400, "Not a JSON")
    if usr is None:
        abort(404)
    for k, v in vals.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(usr, k, v)
    storage.save()
    return(jsonify(usr.to_dict()), 200)
