#!/usr/bin/python3
'''create route for cities'''
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, abort
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        res = []
        for obj in state.cities:
            res.append(obj.to_dict())
        return jsonify(res)
