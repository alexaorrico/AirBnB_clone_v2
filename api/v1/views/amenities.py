#!/usr/bin/python3
""" Routes for states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import amenity
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=["GET"], strict_slashes=False)
def amenities(amenity_id=None):
    """Get specific id amenity or all amenities"""
    if amenity_id is None:
        amenities = storage.all("Amenity")
        all_amenities = [value.to_dict() for key, value in amenities.items()]
        return jsonify(all_amenities), 200
    all_amenities = storage.get(Amenity, amenity_id)
    if all_amenities is None:
        abort (404)
    return jsonify(all_amenities.to_dict()), 200
    

@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity based on ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def post_amenity():
    """Creates Amenity"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data.keys():
        abort(400, "Missing name")
    new_data = Amenity(**data)
    new_data.save()
    return (jsonify(new_data.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
