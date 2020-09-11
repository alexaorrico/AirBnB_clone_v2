#!/usr/bin/python3
""" Amenities view """


from flask import jsonify, make_response, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrives all amenities objects"""
    objects = storage.all(Amenity)
    list_values = []
    for key, value in objects.items():
        list_values.append(value.to_dict())
    return jsonify(list_values)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """ Get amenities by ID """
    state_object = storage.get(Amenity, amenity_id)
    result = None
    if state_object.__class__.__name__ == 'Amenity':
        result = jsonify(state_object.to_dict())
    else:
        result = abort(404)
    return result


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenities(amenity_id):
    """ DELETE amenity by ID """
    state_object = storage.get(Amenity, amenity_id)
    result = None
    if state_object.__class__.__name__ == 'Amenity':
        storage.delete(state_object)
        storage.save()
        result = make_response(jsonify({}), 200)
    else:
        result = abort(404)
    return result


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """ ADD amenities """
    if request.is_json:
        data = request.get_json()
        if 'name' not in data:
            result = jsonify({'error': 'Missing name'}), 400
        else:
            new_object = Amenity(**data)
            storage.new(new_object)
            storage.save()
            result = jsonify(new_object.to_dict()), 201
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenities(amenity_id):
    """ PUT amenities """
    amenity_object = storage.get(Amenity, amenity_id)
    if not amenity_object.__class__.__name__ == 'Amenity':
        return abort(404)
    if request.is_json:
        data = request.get_json()
        for key, value in data.items():
            setattr(amenity_object, key, value)
        storage.save()
        result = jsonify(amenity_object.to_dict()), 200
    else:
        result = jsonify({'error': 'Not a JSON'}), 400
    return result
