#!/usr/bin/python3
""" Amenity Module """
from api.v1.views import app_views
from flask import Flask
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenity_list():
    """ Method: Retrieve list of all amenity objects """


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenity_object():
    """ Method: Retrieve an amenity object """


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_create():
    """ Method: Create an amenity object """


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def amenity_update():
    """ Method: Update an amenity object """