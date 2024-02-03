#!/usr/bin/python3
"""amenities view"""
from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenities():
    """display all amenities"""
    return jsonify([obj.to_dict() for obj in storage.all(Amenity).values()])


@app_views.route('/amenities/<id>', methods=['GET'])
def amenity_by_id(id):
    """display amenity by id"""
    amenity = storage.get(Amenity, id)
    if amenity:
        return amenity.to_dict()
    abort(404)


@app_views.route('/amenities/<id>', methods=['DELETE'])
def delete_amenity(id):
    """delete a amenity by its id"""
    amenity = storage.get(Amenity, id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return {}
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """create a new amenity"""
    if request.is_json:
        data = request.get_json()
        if not data.get('name'):
            abort(400, 'Missing name')
        new_amenity = Amenity(**data)
        new_amenity.save()
        return new_amenity.to_dict(), 201

    abort(400, 'Not a JSON')


@app_views.route('amenities/<id>', methods=['PUT'])
def update_amenity(id):
    """update a amenity by its id"""
    amenity = storage.get(Amenity, id)
    if not amenity:
        return abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    storage.save()
    return amenity.to_dict()
