#!/usr/bin/python3
""" amenities """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """ retrieves all amenity objects """
    output = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        output.append(amenity.to_dict())
    return (jsonify(output))


@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def get_an_amenity(amenity_id):
    """ retrieves one unique amenity object """
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        if amenity.id == amenity_id:
            output = amenity.to_dict()
            return (jsonify(output))
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def del_an_amenity(amenity_id):
    """ delete one unique amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
