#!/usr/bin/python3
"""view of Amenity objects"""
from api.v1.views import app_views
from models import storage, amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """get all Amenity objects"""
    objs = [a.to_dict() for a in storage.all('Amenity').values()]
    if len(objs) == 0:
        return abort(404)
    return objs
