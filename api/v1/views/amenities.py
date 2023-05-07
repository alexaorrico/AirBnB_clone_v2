#!/usr/bin/python3
""" amenities view """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_amenity(amenity_id=None):
    """ get all Amenities or just one Amenity """
    if amenity_id is None:
        amenities = [amenity.to_dict() for amenity
                     in storage.all("Amenity").values()]
        return jsonify(amenities)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ delete an Amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ create an Amenity """
    try:
        req = request.get_json()
    except ValueError:
        req = None
    if req is None:
        abort(400, {'Not a JSON'})
    if 'name' not in req:
        abort(400, {'Missing name'})
    amenity = Amenity(**req)
    amenity.save()
    return amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """ update an Amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    try:
        req = request.get_json()
    except ValueError:
        req = None
    if req is None:
        abort(400, {'Not a JSON'})
    for key, val in req.items():
        if key not in ('id', 'created_at', 'updates_at'):
            setattr(amenity, key, val)
    amenity.save()
    return amenity.to_dict()
