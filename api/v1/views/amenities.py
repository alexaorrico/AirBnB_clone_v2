#!/usr/bin/python3
'''Amenities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''Methods allowed for the amenities endpoint.'''


@app_views.route('/amenities', methods=ALLOWED_METHODS)
@app_views.route('/amenities/<amenity_id>', methods=ALLOWED_METHODS)
def handle_amenities(amenity_id=None):
    '''The method handler for the amenities endpoint.
    '''
    handlers = {
        'GET': get_amenities,
        'DELETE': remove_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_amenities(amenity_id=None):
    '''Gets the amenity with the given id or all amenities.
    '''
    amenity_v_list = storage.all(Amenity).values()
    if amenity_id:
        v_res = list(filter(lambda x: x.id == amenity_id, amenity_v_list))
        if v_res:
            return jsonify(v_res[0].to_dict())
        raise NotFound()
    amenity_v_list = list(map(lambda x: x.to_dict(), amenity_v_list))
    return jsonify(amenity_v_list)


def remove_amenity(amenity_id=None):
    '''Removes a amenity with the given id.
    '''
    amenity_v_list = storage.all(Amenity).values()
    v_res = list(filter(lambda x: x.id == amenity_id, amenity_v_list))
    if v_res:
        storage.delete(v_res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_amenity(amenity_id=None):
    '''Adds a new amenity.
    '''
    v_data = request.get_json()
    if type(v_data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in v_data:
        raise BadRequest(description='Missing name')
    amenity_v = Amenity(**v_data)
    amenity_v.save()
    return jsonify(amenity_v.to_dict()), 201


def update_amenity(amenity_id=None):
    '''Updates the amenity with the given id.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    amenity_v_list = storage.all(Amenity).values()
    v_res = list(filter(lambda x: x.id == amenity_id, amenity_v_list))
    if v_res:
        v_data = request.get_json()
        if type(v_data) is not dict:
            raise BadRequest(description='Not a JSON')
        pre_v_amenity = v_res[0]
        for key, value in v_data.items():
            if key not in xkeys:
                setattr(pre_v_amenity, key, value)
        pre_v_amenity.save()
        return jsonify(pre_v_amenity.to_dict()), 200
    raise NotFound()
