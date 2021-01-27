#!/usr/bin/python3
"""this is a test string"""

from flask import request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<c_id>/places",
                 strict_slashes=False,
                 methods=["GET", "POST"])
def places_base(c_id):
    """this is a test string"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "POST":
        return {"POST": "Not implemented"}


@app_views.route("/places/<p_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def places_id(p_id):
    """this is a test string"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "DELETE":
        return {"DELETE": "Not implemented"}
    if request.method == "PUT":
        return {"PUT": "Not implemented"}
