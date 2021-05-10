#!/usr/bin/python3
"""
Handles Amenity class RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import amenity, storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves a list of all amenity objects"""
    amenity_list = []
    for amenity in storage.all("Amenity").values():
        amenity_list.append(amenity.to_dict())

    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """Returns a single amenity object based on amenity id
       404 error if not found.
    """
    amenity_ob = storage.get("Amenity", amenity_id)
    if amenity_ob is None:
        abort(404)
    else:
        return jsonify(amenity_ob.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Deletes an amenity ojbect"""
    amenity_ob = storage.get("Amenity", amenity_id)
    if amenity_ob is None:
        abort(404)
    else:
        storage.delete(amenity_ob)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an amenity"""
    req = request.get_json(silent=True)
    if req is None:
        abort(400, "Not a JSON")
    elif "name" not in req.keys():
        abort(400, "Missing name")
    else:
        new_amenity_ob = Amenity(**req)
        storage.new(new_amenity_ob)
        storage.save()
        return jsonify(new_amenity_ob.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity ojbect"""
    amenity_ob = storage.get("Amenity", amenity_id)
    if amenity_ob is None:
        abort(404)

    req = request.get_json(silent=True)
    if req is None:
        abort(400, "Not a JSON")
    else:
        for key, value in req.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(amenity_ob, key, value)
        storage.save()
        return jsonify(amenity_ob.to_dict()), 200
