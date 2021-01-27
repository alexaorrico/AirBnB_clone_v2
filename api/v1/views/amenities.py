#!/usr/bin/python3
"""x"""

from flask import request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET", "POST"])
def amenities_base():
    """x"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "POST":
        return {"POST": "Not implemented"}


@app_views.route("/amenities/<a_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def amenities_id(a_id):
    """x"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "DELETE":
        return {"DELETE": "Not implemented"}
    if request.method == "PUT":
        return {"PUT": "Not implemented"}
