#!/usr/bin/python3
"""amenitys"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id=None):
    """get amenity object"""
    if amenity_id is None:
        Namenitylist = []
        for item in storage.all(Amenity).values():
            Namenitylist.append(item.to_dict())
        return jsonify(Namenitylist)
    elif storage.get(Amenity, amenity_id):
        return jsonify(storage.get(Amenity, amenity_id).to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id=None):
    """Delete amenity object"""
    if storage.get(Amenity, amenity_id):
        storage.delete(storage.get(Amenity, amenity_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Add amenity object"""
    if request.get_json() is None:
        abort(400, "Not a JSON")
    elif "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        new_amenity = Amenity(**request.get_json())
        storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id=None):
    """Update amenity object"""
    if storage.get("Amenity", amenity_id) is None:
        abort(404)
    if request.get_json() is None:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(storage.get("Amenity", amenity_id), key, value)
    storage.save()
    return jsonify(storage.get("Amenity", amenity_id).to_dict()), 200
