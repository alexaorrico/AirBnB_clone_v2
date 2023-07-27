#!/usr/bin/python3
""" Endpoints for amenity related
    interactions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenitys():
    """retrieve all amenity objects and
       create new amenity objects
    """
    if request.method == 'GET':
        all_amenities = list(storage.all(Amenity).values())
        all_amenities = [amenity.to_dict() for amenity in all_amenities]
        return jsonify(all_amenities)

    if request.method == 'POST':
        data = get_json(request)
        if not data:
            return make_response('Not a JSON\n', 400)
        if 'name' not in data.keys():
            return make_response('Missing name\n', 400)
        new_amenity = Amenity(**data)
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def amenity_by_id(amenity_id):
    """search for a amenity with given id and:
        1. return it
        2. update it
        3. delete it
       depending on the method
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = get_json(request)
        if not data:
            return make_response('Not a JSON\n', 400)
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)


def get_json(request):
    """check if body has json data
       and handles errors reponses
    """
    #  exception handling to avoid calling
    #  on_json_loading_failed()
    try:
        data = request.get_json()
    except Exception:
        data = None
    return data
