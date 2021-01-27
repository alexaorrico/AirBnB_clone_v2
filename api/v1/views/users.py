#!/usr/bin/python3
"""this is a test string"""

from flask import request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET", "POST"])
def users_base():
    """this is a test string"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "POST":
        return {"POST": "Not implemented"}


@app_views.route("/users/<u_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def users_id(u_id):
    """this is a test string"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "DELETE":
        return {"DELETE": "Not implemented"}
    if request.method == "PUT":
        return {"PUT": "Not implemented"}
