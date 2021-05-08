#!/usr/bin/python3
'''creates a new view for Amenity objects'''
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, request, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getter_amenities():
    '''getter_amenites - gets all Amenity objects'''
    new_list = []
    allamenities = list(storage.all("Amenity").values())

    for amenity in allamenities:
        new_list.append(amenity.to_dict())
    return jsonify(new_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def getter_amenity_id(amenity_id):
    '''getter_id - gets all Amenity objects by id'''
    try:
        amenity = storage.get(Amenity, amenity_id).to_dict()
        return jsonify(amenity)
    except Exception:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleter_amenity(amenity_id):
    '''deleter_id - delete an object by id'''
    id = storage.get(Amenity, amenity_id)

    if id is not None:
        storage.delete(id)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post_amenity():
    '''post_amenity - create an amenity object with post'''
    try:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        body_dict = request.get_json()
        if "name" not in body_dict:
            return jsonify({"error": "Missing name"}), 400
        amenity = Amenity(name=body_dict["name"])
        amenity.save()
        return jsonify(amenity.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    '''put_amenity - updates a amenity object by id'''
    amenityId = storage.get(Amenity, amenity_id)

    if amenityId is None:
        abort(404)
    body_dict = request.get_json()
    if body_dict is None:
        abort(400, "Not a JSON")
    body_dict.pop("id", None)
    body_dict.pop("created_at", None)
    body_dict.pop("updated_at", None)
    for key, value in body_dict.items():
        setattr(amenityId, key, value)
    amenityId.save()
    return jsonify(amenityId.to_dict()), 200
