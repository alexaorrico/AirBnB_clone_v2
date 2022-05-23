#!/usr/bin/python3
"""Amenities api"""
from api.v1.views import app_views
from models.amenity import Amenity
from api.v1.views.cosasc import do


@app_views.route("/amenities", methods=["GET", "POST"])
def amenities():
    """Get or create """
    return do(Amenity)


@app_views.route("/amenities/<id>", methods=["GET", "PUT", "DELETE"])
def amenities_id(id):
    """Modifyy"""
    return do(Amenity, id)
