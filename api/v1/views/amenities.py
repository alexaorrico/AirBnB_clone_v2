#!/usr/bin/python3
"""A scripts that handle RestAPI action for state"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, CNC


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """Route that fetch/Add Amenity Objects"""
    if request.method == 'GET':
        amenities = storage.all('Amenity')
        amenities_list = list(amenity.to_json() for amenity in amenities.values())
        return jsonify(amenities_list)

    if request.method == 'POST':
        request_json = request.get_json()
        if request_json is None:
            abort(404, 'Not a JSON')
        if request_json.get("name") is None:
            abort(400, 'Missing Name')
        Amenity = CNC.get("Amenity")
        new_amenity_obj = Amenity(**request_json)
        new_amenity_obj.save()
        return jsonify(new_amenity_obj.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def get_amenities_by_id(amenity_id):
    """Route that handles retrieving and deleteing
       a Amenity base on the amenity_id
       Parameter:
        amenity_id: string, state id to retrieve or delete
       Return:
        GET - The retrived amenity in json
        DELETE - empty json
        PUT: updated amenity object
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(amenity.to_json())
    if request.method == 'DELETE':
        amenity.delete()
        del amenity
        return jsonigy({})
    if request.method == 'PUT':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        amenity = bm_update(request_json)
        return jsonify(amenity.to_json()), 200
