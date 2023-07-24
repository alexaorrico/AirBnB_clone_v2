#!/usr/bin/python3
""" View for amenities """
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_no_id():
    """ Gets an amenity if no id has been provided """
    slist = []
    states = storage.all(Amenity).values()
    for state in states:
        slist.append(state.to_dict())
    return jsonify(slist)

