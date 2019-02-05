#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage
# from models import State
# from models.base_model import BaseModel


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def showStates():
    """ Shows all states in the file storage """
    count_l = []
    for value in storage.all("State").values():
        count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def showStates():
    """ show the state of the ID or 404 if not found """
    count_l = []
    for value in storage.all("State").values():
        count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/states', strict_slashes=False, methods=['DELETE'])
def showStates():
    """ deletes the state with the id and """
    count_l = []
    for value in storage.all("State").values():
        count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def showStates():
    """ Posts an updated state to the database """
    count_l = []
    for value in storage.all("State").values():
        count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/states', strict_slashes=False, methods=['PUT'])
def showStates():
    """ updates a new state in the data base """
    count_l = []
    for value in storage.all("State").values():
        count_l.append(value.to_dict())
    return(jsonify(count_l))
