#!/usr/bin/python3
'''
methods and routes for working with amenity data
'''
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    ''''''
    all_amenities = []
    for i in storage.all("Amenity").values():
        all_amenities.append(i.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_one_amenity(amenity_id):
    ''''''
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    else:
        return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    ''''''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return ({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    ''''''
    amenity = request.get_json()
    if amenity is None:
        abort(400, 'not a JSON')
    if 'name' not in amenity:
        abort(400, 'Missing Name')
    new_amenity = Amenity(**amenity)
    storage.net(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    ''''''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_info = request.get_json()
    if amenity_info is None:
        abort(400, 'not a JSON')
    for key, value in amenity_info.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(amenity, key, value)
    storage.save()
    all_amenities = amenity.to_dict()
    return jsonify(all_amenities), 200
