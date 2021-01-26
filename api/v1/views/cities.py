#!/usr/bin/python3

from flask import request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<s_id>/cities", strict_slashes=False, methods=["GET", "POST"])
def cities_base(s_id):
    """x"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "POST":
        return {"POST": "Not implemented"}


@app_views.route("/cities/<c_id>", strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def cities_id(c_id):
    """x"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "DELETE":
        return {"DELETE": "Not implemented"}
    if request.method == "PUT":
        return {"PUT": "Not implemented"}
