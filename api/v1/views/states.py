#!/usr/bin/python3
"""
    state endpoint
"""
from api.v1.views import app_views
from models.state import State
from api.v1.views.general import do


@app_views.route("/states", methods=["GET", "POST"])
def states():
    """ list or create """
    return do(State)


@app_views.route("/states/<id>", methods=["GET", "PUT", "DELETE"])
def states_id(id):
    """ modify """
    return do(State, id)
