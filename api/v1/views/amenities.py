#!/usr/bin/python3
""" Amenity objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def allAmenity(state_id):
    '''Retrieves the list of all Amenity objects of a State:
    GET /api/v1/states/<state_id>/amenities'''

    allAmenity = storage.all('Amenity', amenity_id)
    listAmenity = []
    for amenity in allAmenity.values():
        listAmenity.append(amenity.to_dict())
    return jsonify(listAmenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def objAmenity(amenity_id):
    '''Retrieves a Amenity object. :
    GET /api/v1/amenities/<amenity_id>'''
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    '''Deletes a Amenities object:
    DELETE /api/v1/amenities/<amenity_id>'''
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/amenities', methods=['POST'],
                 strict_slashes=False)
def createAmenity(state_id):
    '''Creates a Amenity:
    POST /api/v1/states/<state_id>/amenities'''
    state = storage.get('State', state_id)
    if state:
        data_request = request.get_json()
        if isinstance(data_request, dict):
            for k in data_request.keys():
                if k == "name":
                    obj = Amenity(**data_request)
                    setattr(obj, 'state_id', state_id)
                    storage.new(obj)
                    storage.save()
                    return jsonify(obj.to_dict()), 201
                else:
                    abort(400, 'Missing name')
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    '''Updates a Amenity object:
    PUT /api/v1/amenities/<amenity_id>'''
    obj = storage.get('Amenity', amenity_id)
    if obj:
        data_request = request.get_json()
        if isinstance(data_request, dict):
            noKeys = ['id', 'state_id', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(obj, key, value)
            obj.save()
            return jsonify(obj.to_dict()), 200
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)
