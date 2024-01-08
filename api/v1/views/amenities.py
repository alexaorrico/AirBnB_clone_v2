#!/usr/bin/python3
"""Amenity view"""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """Retrieves the list of all amenity objects"""
    from models import storage
    from models.amenity import Amenity
    amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a amentiy object"""
    from models import storage
    from models.amenity import Amenity
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a amenity object"""
    from models import storage
    from models.amenity import Amenity
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a amenity"""
    from models import storage
    from models.state import State
    from models.amenity import Amenity
    from flask import request

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400

    amenity = Amenity(**request.get_json())
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates a amenity object"""
    from models import storage
    from models.amenity import Amenity
    from flask import request
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
