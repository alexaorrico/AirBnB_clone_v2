#!/usr/bin/python3

"""
Create a new view for City objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ Returns all cities objects of a certain list """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    cList = []
    for c in cities:
        cList.append(c.to_dict())
    return jsonify(cList)
