#!/usr/bin/python3
"""Flask route module for amenities"""
from api.v1.views import app_views, validate_model, get_json
from flask import jsonify
from models import storage, class_richard


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_no_id_get(amenity_id=None):
    """amenities route - no id GET scenario"""
    all_amenities = storage.all('Amenity')
    all_amenities = [obj.to_dict() for obj in all_amenities.values()]
    return jsonify(all_amenities)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities_no_id_post(amenity_id=None):
    """amenities route - no id POST scenario"""
    req_json = get_json(['name'])
    Amenity = class_richard.get('Amenity')
    new_object = Amenity(**req_json)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_with_id_get(amenity_id=None):
    """amenities route - id given GET scenario"""
    amenity_obj = validate_model('Amenity', amenity_id)
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenities_with_id_del(amenity_id=None):
    """amenities route - id given DELETE scenario"""
    amenity_obj = validate_model('Amenity', amenity_id)
    amenity_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenities_with_id_put(amenity_id=None):
    """amenities route - id given PUT scenario"""
    amenity_obj = validate_model('Amenity', amenity_id)
    req_json = get_json()
    for key, value in req_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
