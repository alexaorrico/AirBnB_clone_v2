#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/users', methods=['GET'])
def listalluser():
    """list of all User objects"""
    temp = []
    for i in storage.all("User").values():
        temp.append(i.to_dict())

    return (temp)

@app_views.route('/users/<user_id>', methods=['DELETE'])
def deleteuser(user_id=None):
    """Deletes a User object"""
    u = storage.get("User", state_id)
    if u is None:
        abort(404)
    else:
        storage.delete(usr)
        storage.save()
        return (jsonify({}), 200)

@app_views.route('/users', methods=['POST'])
def createuser():
    """Creates a User"""
    u = storage.request.get_json("State", silent=True)
    if u == None:
        return (400, "Not a JSON")
    elif "email" not in  u.keys():
        return (400, "Missing email")
    elif "password" not in u.keys():
        return (400, "Missing password")
    else:
        return (jsonify({}), 201)

@app_views.route('/users/<user_id>', method=['PUT'])
def updateuser(user_id=None):
    """Updates a User object"""
    usr = storage.get("User", state_id)
    if usr is None:
        abort(404)
    u = storage.request.get_json("User", silent=True)
    elif u == None:
        abort(400, "Not a JSON")
    else:
        for i, j in u.items:
            if i in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(usr, i, j)
            storage.save()
            temp = usr.to_dict()
            return (jsonify(temp), 200)
