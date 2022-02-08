#!/usr/bin/python3
""" Amenity objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def allAmenity():
    '''Retrieves the list of all Amenity objects of a State:
    GET /api/v1/states/<state_id>/amenities'''

    allAmenity = storage.all(Amenity)
    listAmenity = []
    for amenity in allAmenity.values():
        listAmenity.append(amenity.to_dict())
    return jsonify(listAmenity)
