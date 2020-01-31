#!/usr/bin/python3
"""
    state endpoint
"""
from api.v1.views import app_views
from models.amenity import Amenity
from api.v1.views.general import do


@app_views.route("/amenities", methods=["GET", "POST"])
def amenities():
    """ list or create """
    return do(Amenity)


@app_views.route("/amenities/<id>", methods=["GET", "PUT", "DELETE"])
def amenities_id(id):
    """ modify """
    return do(Amenity, id)
