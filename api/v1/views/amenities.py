#!/usr/bin/python3
""" Show, Delete, Create and Update amenities """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenities(amenity_id=None):
    """ Endpoint that retrieves all amenities
        or retrieves one amenity by id

        amenity_id: id of the amenity to retrieve
    """
    all_amenities = storage.all('Amenity')
    if not amenity_id:
        amenity_info = []
        for amenity in all_amenities.values():
            amenity_info.append(amenity.to_dict())
        return jsonify(amenity_info)
    else:
        amenity = "Amenity.{}".format(amenity_id)
        if amenity in all_amenities:
            amenity = all_amenities[amenity]
            return jsonify(amenity.to_dict())
        else:
            abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Endpoint that deletes a specific amenity
        with the id

        amenity_id : id of the amenity to delete
    """
    all_amenities = storage.all('Amenity')
    amenity = "Amenity.{}".format(amenity_id)
    if amenity in all_amenities:
        amenity = all_amenities[amenity]
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """ Endpoint that creates a amenity
        with the information given
    """
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    if 'name' not in info:
        abort(400, 'Missing name')
    amenity = Amenity(name=info['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id >', strict_slashes=False,
                 methods=['PUT'])
def modify_amenity(amenity_id):
    """ An endpoint that modifies a specific
    amenity with the id
    """
    info = request.get_json()
    if not info:
        abort(400, 'Not a JSON')
    all_amenities = storage.all('Amenity')
    amenity_id = "Amenity.{}".format(amenity_id)
    if amenity_id in all_amenities:
        amenity = all_amenities[amenity_id]
        for key, value in info.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(400)
