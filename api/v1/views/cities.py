#!/usr/bin/python3
""" New City view """

from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ Returns all cities linked to a particular city """
    state_obj = storage.get(State, state_id)
    if state_obj:
        for city in state_obj
