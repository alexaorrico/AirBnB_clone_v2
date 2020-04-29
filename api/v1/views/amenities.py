#!/usr/bin/python3
"""Create a new view for amenities"""


from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenities(amenity_id=None):
    """view for State objects that handles all default RestFul API actions"""
    if amenity_id:
        amenity_id = "Amenity.{}".format(amenity_id)
        all_Amenity = storage.all('Amenity')
        if amenity_id in all_Amenity:
            return jsonify(all_Amenity[amenity_id].to_dict())
        else:
            abort(404)
    else:
        amenityList = []
        all_amenities = storage.all('Amenity')
        for amenity in all_amenities.values():
            amenityList.append(amenity.to_dict())
        return jsonify(amenityList)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def amenities_delete(amenity_id=None):
    id_amenity = storage.get('Amenity', amenity_id)
    if amenity_id is None:
        abort(404)
    storage.delete(id_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    res = request.get_json()
    if 'name' not in res:
        abort(400, 'Missing name')
    if res is None:
        abort(400, 'Not a JSON')
    amenity = Amenity(name=res['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_amenity(amenity_id):
    """ An endpoint that modifies an existing amenity """
    res = request.get_json()
    if res is None:
        abort(400, 'Not a JSON')
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    for k, v in res.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
