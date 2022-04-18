#!/usr/bin/python3
"""New view for Amenity object that handles all default Restfullapi actions"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenity_objs():
    """Retrieves the list of all Amenity Objects"""
    amenities_objs = storage.all(Amenity).values()
    return jsonify([obj.to_dict() for obj in amenities_objs])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id=None):
    """Retrieves an Amenity object by its id"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        return jsonify(amenity_obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Deletes an Amenity object by its id"""
    amenity_objs = storage.get(Amenity, amenity_id)
    if amenity_objs:
        storage.delete(amenity_objs)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenity_post(state_id=None):
    """Create an Amenity object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    dict_body = request.get_json()
    new_amenity = Amenity(**dict_body)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_put(amenity_id=None):
    """Update Amenity object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    dict_body = request.get_json()
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        for key, value in dict_body.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(amenity_obj, key, value)
        storage.save()
        return make_response(jsonify(amenity_obj.to_dict()), 200)
    else:
        return abort(404)
