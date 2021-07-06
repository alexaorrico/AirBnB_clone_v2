#!/usr/bin/python3
"""View for Amenity objects that handles all default RestFul API actions:"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects:
        GET /api/v1/amenities
    """
    amenities = []
    all_amenities = storage.all(Amenity).values()

    for each in all_amenities:
        amenities.append(each.to_dict())

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenities_by_id(amenity_id):
    """ Retrieves a Amenity object:
        GET /api/v1/amenities/<amenity_id>
    """
    amenitie = storage.get(Amenity, amenity_id)

    if amenitie is None:
        abort(404)

    return jsonify(amenitie.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenitie(amenity_id):
    """ Deletes a Amenity object:
        DELETE /api/v1/amenities/<amenity_id>
    """
    amenitie = storage.get(Amenity, amenity_id)

    if amenitie is None:
        abort(404)

    storage.delete(amenitie)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['POST'])
def create_amenitie():
    """ Creates a Amenity:
        POST /api/v1/amenities
    """
    jsonRequest = request.get_json()

    if not jsonRequest:
        return jsonify({'error': 'Not a JSON'}), 400

    elif 'name' not in jsonRequest:
        return jsonify({'error': 'Missing name'}), 400

    else:
        _amenitie = Amenity(**jsonRequest)
        storage.new(_amenitie)
        storage.save()
        return jsonify(_amenitie.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a Amenity object:
        PUT /api/v1/amenities/<amenity_id>
    """
    obj = storage.get(Amenity, amenity_id)
    jsonRequest = request.get_json()

    if not jsonRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    if obj:
        for key, value in jsonRequest.items():
            setattr(obj, key, value)
        storage.save()

        return jsonify(obj.to_dict()), 200
    else:
        abort(404)
