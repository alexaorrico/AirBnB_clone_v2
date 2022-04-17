#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API"""
from models import storage, state
from flask import abort, jsonify


@app_views.route('/states', methods=['GET'])
def listallState():
    """list of all State objects"""
    temp = []
    for i in storage.all("State").values():
        temp.append(j.to_dict())

    return (temp)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def deletestate():
    """Deletes a State object"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)
