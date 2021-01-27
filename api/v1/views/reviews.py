#!/usr/bin/python3

from flask import request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/places/<p_id>/reviews",
                 strict_slashes=False,
                 methods=["GET", "POST"])
def reviews_base(p_id):
    """x"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "POST":
        return {"POST": "Not implemented"}


@app_views.route("/reviews/<r_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def reviews_id(r_id):
    """x"""
    if request.method == "GET":
        return {"GET": "Not implemented"}
    if request.method == "DELETE":
        return {"DELETE": "Not implemented"}
    if request.method == "PUT":
        return {"PUT": "Not implemented"}
