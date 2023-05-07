#!/usr/bin/python3
"""objects that handles all RESTFUL API actions for amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieves a list of all amenities"""
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(ammenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """returns a specific amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_amenity(amenity_id):
    """creates an amenity"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if name not in data:
        return jsonify({'error': 'Missing name'}), 400

    amenity = Amenity(name=data['name'])
    amenity.save()
    return jsonify(amenity.to_dic(), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    ignore = ['id', 'created_at', 'updated_at']
    if not amenity:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
