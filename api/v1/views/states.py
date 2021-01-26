#!/usr/bin/python3

from flask import request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET", "POST"])
def states_base():
    """x"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "POST":
        return {"POST": "Not implemented"}


@app_views.route("/states/<id>", strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def states_id(id):
    """x"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "DELETE":
        return {"DELETE": "Not implemented"}
    if request.method == "PUT":
        return {"PUT": "Not implemented"}
