#!/usr/bin/python3
"""Create a new view for amenities"""


from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """ An endpoint that returns all amentities """
    amenitieslist = []
    amenities = storage.all('Amenity')
    for amenity in amenities.values():
        amenitieslist.append(amenity.to_dict())
    return jsonify(amenitieslist)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    """ An endpoint that returns a specific amenity """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    else:
        return(jsonify(amenity.to_dict()))


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    res = request.get_json()
    if res is None:
        abort(400, 'Not a JSON')
    if 'name' not in res:
        abort(400, 'Missing name')
    amenity = Amenity(name=res['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_amenity(amenity_id):
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
