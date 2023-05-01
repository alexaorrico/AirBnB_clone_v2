#!/usr/bin/python3

"""
This module defines the Flask routes that handle requests related to amenities
"""

from flask import abort, jsonify, request
from flasgger.utils import swag_from
from api.v1.views import app_views
from models import storage, CNC

# Define the route for GET and POST requests to /amenities/
@app_views.route('/amenities/', methods=['GET', 'POST'])
@swag_from('documentation/amenities_no_id.yml', methods=['GET', 'POST'])
def amenities_no_id(amenity_id=None):
    """
    Handle GET and POST requests to the /amenities/ route
    """
    if request.method == 'GET':
        all_amenities = storage.all('Amenity')
        amenities_json = [obj.to_json() for obj in all_amenities.values()]
        return jsonify(amenities_json)

    if request.method == 'POST':
        json_data = request.get_json()
        if json_data is None:
            abort(400, 'Invalid JSON data')
        if json_data.get('name') is None:
            abort(400, 'Missing name field')
        AmenityClass = CNC.get('Amenity')
        new_amenity = AmenityClass(**json_data)
        new_amenity.save()
        return jsonify(new_amenity.to_json()), 201


# Define the route for GET, PUT, and DELETE requests to /amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
@swag_from('documentation/amenities_id.yml', methods=['GET', 'PUT', 'DELETE'])
def amenities_with_id(amenity_id=None):
    """
    Handle GET, PUT, and DELETE requests to the /amenities/<amenity_id> route
    """
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404, 'Amenity not found')

    if request.method == 'GET':
        return jsonify(amenity_obj.to_json())

    if request.method == 'PUT':
        json_data = request.get_json()
        if json_data is None:
            abort(400, 'Invalid JSON data')
        amenity_obj.bm_update(json_data)
        return jsonify(amenity_obj.to_json()), 200

    if request.method == 'DELETE':
        amenity_obj.delete()
        del amenity_obj
        return jsonify({}), 200
