#!/usr/bin/python3
"""Module with the view for State objects"""
from api.v1.views import app_views
from models.state import State
from models import storage
import json


@app_views.route('/states', strict_slashes=False)
def states():
    """"""
    states = storage.all(State).values()
    print(states)
    return json.dumps(states, indent=4)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'],
                 strict_slashes=False)
def states_id(state_id):
    pass
