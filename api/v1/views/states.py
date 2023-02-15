#!/usr/bin/python3
""" New view for State that handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import jsonify
import json
from models import storage


cls = 'State'
@app_views.route('/states', methods=['GET'])
def states():
    """returns State object or collection"""
    states = []
    objs = storage.all(cls)
    for key, val in objs.items():
        obj_dict = val.to_dict()
        states.append(obj_dict)
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def stateid(state_id):
    """Retrieves a single object if present or rase 404"""
    obj = storage.get(cls,state_id)
    obj_dict = obj.to_dict()
    # not yet handled 404 case
    return jsonify(obj_dict)
