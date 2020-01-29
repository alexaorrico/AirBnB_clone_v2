#!/usr/bin/python3
from flask import request, abort, jsonify
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    Creates a State: POST /api/v1/states
    """
    if request.method == 'GET':
        list_amenities = []
        amenities = storage.all('Amenity').values()
        for amenity in amenities:
            list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)

    if request.method == 'POST':
        request_json = request.get_json()
        if not request_json:
            return jsonify(error='Not a JSON')
        if 'name' not in request_json:
            return jsonify(error='Missing name')
        amenity = Amenity(**request_json)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def amenity(amenity_id=None):
    """
    Retrieves the list of all Amenity objects: GET /api/v1/states
    Creates a State: POST /api/v1/states
    """
    if request.method == 'GET':
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            return jsonify(amenity.to_dict())
        abort(404)

    if request.method == 'DELETE':
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        abort(404)

    if request.method == 'PUT':
        request_json = request.get_json()
        if not isinstance(request_json, dict):
            return jsonify(error='Not a JSON')
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            for key, value in request_json.items():
                if key not in ["__class__", "id", "created_at", "updated_at"]:
                    setattr(amenity, key, value)
            storage.save()
            return jsonify(amenity.to_dict()), 200
        abort(404)
