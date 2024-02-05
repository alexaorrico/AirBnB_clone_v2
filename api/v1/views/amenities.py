#!/usr/bin/python3
'''amenities route'''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    '''retrieve all amenity'''
    am = [am.to_dict() for am in storage.all(Amenity).values()]

    return jsonify(am)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    '''retrieve amenity by id'''
    am = storage.get(Amenity, amenity_id)

    if am is None:
        abort(404)

    am = am.to_dict()

    return jsonify(am)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''delere amenity by id'''
    am = storage.get(Amenity, amenity_id)

    if am is None:
        abort(404)

    am.delete()
    storage.save()

    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''creates an amenity instance'''
    data = request.get_json()

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    create = Amenity(**data)

    create.save()
    create = create.to_dict()

    return (jsonify(create), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''update amenity by id'''
    data = request.get_json()
    
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    am = storage.get(Amenity, amenity_id)

    if am is None:
        abort(404)

    for key, value in data.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(am, key, value)
 
    storage.save()
    am = am.to_dict()

    return jsonify(am), 200
