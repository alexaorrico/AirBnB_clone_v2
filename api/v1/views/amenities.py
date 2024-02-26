#!/usr/bin/python3
"""States"""


from flask import jsonify, Response, abort, request, make_response
from werkzeug.exceptions import BadRequest
import json
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all amenity"""
    amenities = [obj.to_dict()
                 for obj in storage.all(Amenity).values()]
    resp = Response(
        response=json.dumps(amenities, indent=4),
        status=200,
        mimetype='application/json'
    )
    return resp


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id):
    """Retrieve a amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new amenity
    """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response("Missing name", 400)

    new_amenity = Amenity(**data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update an existing amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        raise BadRequest('Not a JSON', 400)
    data = request.get_json(silent=True)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
