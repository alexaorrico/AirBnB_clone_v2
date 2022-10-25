#!/usr/bin/python3
""" Flask views for the Amenities resource """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """ An endpoint that returns all amentities """
    rlist = []
    amenities = storage.all('Amenity')
    for amenity in amenities.values():
        rlist.append(amenity.to_dict())
    return jsonify(rlist)


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
    """ An endpoint that deletes a specific amenity """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """ An endpoint that creates a new amenitiuy """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'name' not in content:
        abort(400, 'Missing name')
    amenity = Amenity(name=content['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_amenity(amenity_id):
    """ An endpoint that modifies an existing amenity """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    for k, v in content.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
