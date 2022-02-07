#!/usr/bin/python3
'''amenities blueprint'''

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getamenities():
    '''get all amenities available'''
    amens = storage.all(Amenity)
    return jsonify([amen.to_dict() for amen in amens.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def getAmenityById(amenity_id=None):
    '''gets amenity by id'''
    if amenity_id is None:
        abort(404)
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    return jsonify(amen.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id=None):
    '''deletes an amenity'''
    if amenity_id is not None:
        res = storage.get(Amenity, amenity_id)
        if res is not None:
            storage.delete(res)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def postAmenity():
    '''posts a new amenity'''
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'name' not in body.keys():
        abort(400, 'Missing name')
    amen = Amenity(**body)
    amen.save()
    return make_response(jsonify(amen.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id=None):
    '''updates a amenity'''
    if amenity_id is None:
        abort(404)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    for key in body.keys():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, body[key])
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
