#!/usr/bin/python3
"""
Create a new view for the link between Place objects and Amenity
objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                  strict_slashes=False)
def retrieve_amenity(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    If the place_id is not linked to any Place object, raise a 404 error
    """


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    """

@app_views('/places/<place_id>/amenities/<amenity_id>', methods=['POST'].
           strict_slashes=False)

def link_place(place_id, amenity_id):
    """
    Links an amenity object to a Place:
    """
