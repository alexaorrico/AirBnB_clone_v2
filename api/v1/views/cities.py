#!/usr/bin/python3
"""
    state endpoint
"""
from api.v1.views import app_views
from models.city import City
from general import do


@app_views.route("/states", methods=["GET", "POST"])
def states():
    """ list or create """
    return do(City, request)


@app_views.route("/states/<id>", methods=["GET", "PUT", "DELETE"])
def states_id(id):
    """ states """
    return do(City, request, id)
