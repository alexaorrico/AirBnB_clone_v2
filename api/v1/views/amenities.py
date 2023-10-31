#!/usr/bin/python3
<<<<<<< HEAD
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
=======
'''
    Create a new view for Amenity objects that handles
    all default RESTFul API actions
'''
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    '''Retrieves Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity =  storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''Creates Amenity Object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    jsonData = request.get_json()
    if 'name' not in jsonData:
        abort(400, 'Missing name')
    amenity = Amenity(**jsonData)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates Amenity Object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, 'Not a JSON')
        jsonData = request.get_json()
        ignoreKeys = ['id', 'created_at', 'updated_at']
        for key, value in jsonData.items():
            if key not in ignoreKeys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(400)
def bad_request(error):
    '''Bad request message handler'''
    res = {'error': 'Bad Request'}
    return jsonify(res), 400
>>>>>>> 5cec450237a0478b5ae5ad06db65d963f857233f
