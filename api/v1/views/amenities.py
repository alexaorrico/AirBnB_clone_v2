#!/usr/bin/python3
"""Routings for amenity-related API requests
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_methods(amenity_id=None):
    """Handle requests to API for amentities
    """
    from models.amenity import Amenity
    amenities = storage.all(Amenity)

    # GET REQUESTS
    if request.method == 'GET':
        if not amenity_id:  # if no id specified, return all
            return jsonify([obj.to_dict() for obj in amenities.values()])

        key = 'Amenity.' + amenity_id
        try:  # if obj exists in dictionary, convert from obj -> dict -> json
            return jsonify(amenities[key].to_dict())
        except KeyError:
            abort(404)  # Amenity with amenity_id does not exist

    # DELETE REQUESTS
    elif request.method == 'DELETE':
        try:
            key = 'Amenity.' + amenity_id
            storage.delete(amenities[key])
            storage.save()
            return jsonify({}), 200
        except:
            abort(404)

    # POST REQUESTS
    elif request.method == 'POST':
        # convert JSON request to dict
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # instantiate, store, and return new Amenity object
        if 'name' in body_request:
            new_amenity = Amenity(**body_request)
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
        else:  # if request does not contain required attribute
            abort(400, 'Missing name')

    # PUT REQUESTS
    elif request.method == 'PUT':
        key = 'Amenity.' + amenity_id
        try:
            amenity = amenities[key]

            # convert JSON request to dict
            if request.is_json:
                body_request = request.get_json()
            else:
                abort(400, 'Not a JSON')

            for key, val in body_request.items():
                if key != 'id' and key != 'created_at' and key != 'updated_at':
                    setattr(amenity, key, val)

            storage.save()
            return jsonify(amenity.to_dict()), 200
        except KeyError:
            abort(404)

    # UNSUPPORTED REQUESTS
    else:
        abort(501)
