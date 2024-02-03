#!/usr/bin/python3
'''amenities route'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    '''retrieve all amenity'''
    am = [am.to_dict() for am in storage.all(Amenity).values()]

    return jsonify(am)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_by_id(amenity_id):
    '''retrieve amenity by id'''
    am = storage.get(Amenity, amenity_id)

    if am is None:
        abort(404)

    am = am.to_dict()

    return jsonify(am)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''delere amenity by id'''
    am = storage.get(Amenity, amenity_id)

    if am is None:
        abort(404)

    storage.delete(am)
    storage.save()

    return {}, 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    '''creates an amenity instance'''
    try:
        data = request.get_json()
    except Exception:
        return jsonify('Not a JSON'), 400

    create = Amenity()

    for key, value in data.items():
        if key != 'name':
            return jsonify('Missing name'), 400
        setattr(create, key, value)

    create = create.to_dict()

    return jsonify(create), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    '''update amenity by id'''
    try:
        data = request.get_json()
    except Exception:
        return jsonify('Not a JSON'), 400

    am = storage.get(Amenity, amenity_id)

    if am is None:
        abort(404)

    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue
        setattr(am, key, value)

    storage.save()
    am = am.to_dict()

    return jsonify(am), 200
