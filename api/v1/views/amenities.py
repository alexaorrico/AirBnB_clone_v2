#!/usr/bin/python3
"""
handles all RESTFUl API actions for Amenities
"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.engine.db_storage import classes


@app_views.route('/amenities', methods=['GET', 'POST'])
def all_amenities():
    """ defines route for api/v1/amenities """
    if request.method == 'GET':
        amenity = [a.to_dict() for a in storage.all('Amenity').values()]
        return jsonify(amenity)

    if request.method == 'POST':
        if not request.json:
            return make_response('Not a JSON', 400)
        if 'name' not in request.json:
            return make_response('Missing name', 400)
        newObj = classes['Amenity']
        newAmenity = newObj(**request.json)
        newAmenity.save()
        return jsonify(newAmenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_by_id(amenity_id):
    """ defines route for api/vi/amenities/<amenity_id> """
    allAmenity = [a for a in storage.all('Amenity').values()]
    amenity = [a for a in allAmenity if a.id == amenity_id]
    if request.method == 'GET':
        if (len(amenity) == 0):
            abort(404)
        return jsonify(amenity[0].to_dict())

    if request.method == 'DELETE':
        if len(amenity) == 0:
            return make_response('Not found', 404)
        storage.delete(amenity[0])
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        if len(amenity) == 0:
            abort(404)
        if not request.json:
            return make_response('Not a JSON', 400)
        data = request.json
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_ap']:
                setattr(amenity[0], key, value)
                amenity[0].save()
        return jsonify(amenity[0].to_dict()), 200
