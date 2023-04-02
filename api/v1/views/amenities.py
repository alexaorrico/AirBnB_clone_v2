#!/usr/bin/python3
""" handles all default RestFul API """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def amenities_view():
    """ return a jsonified amenity objects """
    amenities_list = []
    for value in storage.all(Amenity).values():
        amenities_list.append(value.to_dict())
    return (jsonify(amenities_list))


@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def amenities_id_view(amenity_id):
    """ returns a jsonified amenity obj by amenity_id """
    get_id = storage.get(Amenity, amenity_id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete amenity obj by amenity_id """
    get_id = storage.get(Amenity, amenity_id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """ creating a amenity object """
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if "name" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    new_amenity_obj = Amenity(**data_req)
    new_amenity_obj.save()
    return (jsonify(new_amenity_obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ updating a amenity object """
    get_id = storage.get(Amenity, amenity_id)
    if get_id is None:
        abort(404)
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for key, value in data_req.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(get_id, key, value)
    get_id.save()
    return (jsonify(get_id.to_dict()), 200)
