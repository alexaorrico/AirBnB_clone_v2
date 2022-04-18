#!/usr/bin/python3
"""Amenity view model"""
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

amenity_objs = storage.all('Amenity')


@app_views.route('/amenities/', methods=['GET'])
def get_amenity():
    """Retrieves a list of all amenity objects."""
    amenities = [obj.to_dict() for obj in amenity_objs.values()]

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_Amenity(amenity_id):
    """Retrieves a Amenity object."""
    amenity_id = "Amenity." + amenity_id

    if amenity_id not in amenity_objs.keys():
        abort(404)

    amenity = amenity_objs.get(amenity_id)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_Amenity(amenity_id):
    """Deletes a specified Amenity model."""
    amenity_id = "Amenity." + amenity_id

    if amenity_id not in amenity_objs.keys():
        abort(404)

    storage.all().pop(amenity_id)
    storage.save()

    return jsonify({}), 200, {'ContentType': 'application/json'}


@app_views.route('/amenities/', methods=['POST'])
def create_Amenity():
    """Creates a new Amenity object."""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.get_json().keys():
        abort(400, 'Missing name')

    amenity = (Amenity(**request.get_json()))
    storage.new(amenity)
    storage.save()
    return amenity.to_dict(), 201, {'ContentType': 'application/json'}


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def update_Amenity(amenity_id):
    """Modifies a Amenity object."""
    amenity_objs = storage.all('Amenity')
    amenity_id = "Amenity." + amenity_id

    if not request.json:
        abort(400, "Not a JSON")
    if amenity_id not in amenity_objs.keys():
        abort(404)

    amenity = Amenity(**request.get_json())

    return amenity.to_dict(), 200, {'ContentType': 'application/json'}
