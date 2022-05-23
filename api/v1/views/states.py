#!/usr/bin/python3
"""State api"""
from api.v1.views import app_views
from models.state import State
from api.v1.views.cosasc import do


@app_views.route("/states", methods=["GET", "POST"])
def states():
    """Get or create method"""
    return do(State)


@app_views.route("/states/<id>", methods=["GET", "PUT", "DELETE"])
def states_id(id):
    """Other route"""
    return do(State, id)
