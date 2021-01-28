#!/usr/bin/python3
"""State objects"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def ret_amenities():
    """ Retrieves amenities """
    list_amenieties = []
    for amenity in storage.all(Amenity).values():
        list_amenieties.append(amenity.to_dict())
    return jsonify(list_amenieties)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def ret_amenity(amenity_id):
    """ Retrieves an amenity """
    single_amenity = storage.get(Amenity, amenity_id)
    if single_amenity is None:
        abort(404)
    return jsonify(single_amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state(amenity_id):
    """Delete a amenity object"""
    amenity_del = storage.get(Amenity, amenity_id)
    if amenity_del:
        storage.delete(amenity_del)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Task 7 :Updates a State object:"""
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    amenity_up = storage.get(Amenity, state_id)
    if amenity_up is None:
        abort(404)
    for key, val in content.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity_up, key, val)
    storage.save()
    return jsonify(amenity_up.to_dict()), 200


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)
