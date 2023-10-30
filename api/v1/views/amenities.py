#!/usr/bin/python3
"""
API Amenity View Module

Defines the API views for the amenity objects, providing RESTful
endpoints to interact with Amenity resources.

Endpoints:
- GET /api/v1/amenities: Retrieves a list of all objects.
- GET /api/v1/amenities/<amenity_id>: Retrieves an object by its ID.
- DELETE /api/v1/amenities/<amenity_id>: Removes an object by its ID.
- POST /api/v1/amenities: Creates a new object.
- PUT /api/v1/amenities/<amenity_id>: Updates an object by its ID.

Each endpoint performs specific actions on Amenity resources and returns
results in JSON format.

HTTP status codes:
- 200: OK: The request has been successfully processed.
- 201: 201 Created: The new resource has been created.
- 400: Bad Request: The server cannot process the request.
- 404: Not Found: The requested resource could not be found on the server.
"""

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves a list of all Amenity objects """
    objs = storage.all('Amenity')
    amenities = []
    for amenity in objs.values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an Amenity object by its ID """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_amenity(amenity_id):
    """ Removes an Amenity object by its ID """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a new Amenity object """
    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})
    if 'name' not in response:
        abort(400, {'Missing name'})

    new_amenity = Amenity(name=response['name'])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an Amenity object by its ID """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, {'Not a JSON'})

    skip_keys = ['id', 'created_at', 'updated_at']
    for k, val in response.items():
        if k not in skip_keys:
            setattr(amenity, k, val)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
