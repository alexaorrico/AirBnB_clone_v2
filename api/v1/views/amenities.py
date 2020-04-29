#!/usr/bin/python3
"""Create a new view for Amenities"""
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False,
                 defaults={'amenity_id': 0})
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id):
    dic = storage.all(Amenity)
    ids = "Amenity." + str(amenity_id)
    if (amenity_id == 0):
        amenities_list = []
        for k, v in dic.items():
            amenities_list.append(v.to_dict())
        return jsonify(amenities_list)
    elif (ids not in dic.keys()):
        abort(404)
    else:
        return jsonify(dic[ids].to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenities_delete(amenity_id=None):
    """Deletes a State object:: DELETE /api/v1/states/state_id"""
    id_amenity = storage.get('Amenity', amenity_id)
    if amenity_id is None:
        abort(404)
    else:
        storage.delete(id_amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenities_create():
    """Creates new states"""
    res = request.get_json()
    if res is None:
        abort(400, "Not a JSON")
    if 'name' not in res:
        abort(400, "Missing name")
    newAmenity = Amenity(name=res['name'])
    storage.new(newAmenity)
    storage.save()
    return jsonify(newAmenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenities_put(amenity_id=None):
    """updates a value from an instance"""
    amenity = storage.get('Amenity', amenity_id)
    res = request.get_json()

    if amenity is None:
        abort(404)
    if res is None:
        abort(400, "Not a JSON")
    for k, v in res.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
