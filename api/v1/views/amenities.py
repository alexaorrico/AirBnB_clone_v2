#!/usr/bin/python3
""" View for amenities """
from flask import jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_no_id():
    """ Gets an amenity if no id has been provided """
    amen_l = []
    amen = storage.all(Amenity).values()
    return jsonify([a.to_dict() for a in amen])

@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id=None):
    """ Gets an amenity when an id is provided """
    amen = storage.all(Amenity)
    a_key = "Amenity." + amenity_id
    if a_key not in amen:
        abort(404)
    return(jsonify(amen[a_key].to_dict()))
