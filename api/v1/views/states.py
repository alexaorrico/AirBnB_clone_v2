#!/usr/bin/python3
from flask import jsonify, abort
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


@app_views.route('/states/<id>', strict_slashes=False, methods=['GET'])
def a_states_id(id):
    for s_id in storage.all('State').values():
        if s_id.id == id:
            return jsonify(s_id.to_dict())
        else:
            return (jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<id>', strict_slashes=False, methods=["DELETE"])
def del_states_id(id):
    for s_id in storage.all('State').values():
        if s_id.id == id:
            return jsonify(s_id.delete())
        else:
            return (jsonify({"error": "Not found"}), 404)
