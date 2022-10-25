#!/usr/bin/pythoon3
""" view for amenity objects """

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    all_amenities = storage.all(Amenity)
    amenities = [amenity.to_dict() for amenity in all_amenities.values():
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        return jsonify(amenity.to_dict())
    except KeyError:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    try:
        amenity = storage.get(Amenity, amenity_id)
        amenity.delete()
        storage.save()
        return jsonify({})
    except KeyError:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity object"""
    try:
        data = request.get_json()
        if data.get("name") is None:
            return make_response(jsonify({"error": "Missing name"}), 400)
        amenity = Amenity(**data)
        amenity.save()
        response = jsonify(amenity.to_dict())
        response.status_code = 201
        return response
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    try:
        data = request.get_json()
        amenity = storage.get(Amenity, amenity_id)
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
