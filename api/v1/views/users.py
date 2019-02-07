#!/usr/bin/python3
"""Routes for User"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def showUser():
    """ Shows all users in the file storage """
    count_l = []
    for value in storage.all("User").values():
        count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET'])
def a_user_id(user_id):
    """ Gets the user and its id if any """
    i = storage.get("User", user_id)
    if i:
        return jsonify(i.to_dict())
    else:
        return (jsonify({"error": "Not found"}), 404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_user_id(user_id):
    """ deletes a user if given the id """
    thing = storage.all('User')
    usee = "User." + user_id
    useee = thing.get(usee)
    if useee is None:
        abort(404)
    else:
        useee.delete()
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def postUser():
    """ creates a new User """
    thing = request.get_json(silent=True)
    if thing is None or not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    use_mail = thing.get("email")
    use_pass = thing.get("password")
    if use_mail is None or len(thing) == 0:
        return (jsonify({"error": "Missing email"}), 400)
    if use_pass is None or len(thing) == 0:
        return(jsonify({"error": "Missing password"}), 400)
    u = User()
    u.email = use_mail
    u.password = use_pass
    u.save()
    return (jsonify(u.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def updateUser(user_id):
    """ updates the user info, specifically name """
    usee = storage.get("User", user_id)
    if usee is None:
        abort(404)
    if not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    thing = request.get_json()
    for key, value in thing.items():
        if key == 'first_name':
            setattr(usee, key, value)
        if key == 'last_name':
            setattr(usee, key, value)
        if key == 'password':
            setattr(usee, key, value)
    usee.save()
    return (jsonify(usee.to_dict()), 200)
