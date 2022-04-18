#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API"""
from models import storage, state
from flask import abort, jsonify, request


@app_views.route('/states', methods=['GET'])
def listallState():
    """list of all State objects"""
    temp = []
    for i in storage.all("State").values():
        temp.append(j.to_dict())

    return (temp)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def deletestate(state_id=None):
    """Deletes a State object"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)

@app_views.route('/states', methods=['POST'])
def createstate():
    """Creates a State"""
    s = storage.request.get_json("State", silent=True)
    if s == None:
        return (400, "Not a JSON")
    elif "name" not in  s.keys():
        return (400, "Missing name")
    else:
        return (jsonify({}), 201)

@app_views.route('/states/<state_id>', method=['PUT'])
def updatestate(state_id=None):
    """Updates a State object"""
    st = storage.get("State", state_id)
    if st is None:
        abort(404)
    s = storage.request.get_json("State", silent=True)
    elif s == None:
        abort(400, "Not a JSON")
    else:
        for i, j in s.items:

