#!/usr/bin/python3
"""amenities view"""
from flask import abort, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenities():
    """display all amenities"""
    return [obj.to_dict() for obj in storage.all(Amenity).values()]


@app_views.route('/amenities/<id>', methods=['GET'])
def amenity_by_id(id):
    """display amenity by id"""
    amenity = storage.get(Amenity, id)
    if amenity:
        return amenity.to_dict()
    return abort(404)


@app_views.route('/amenities/<id>', methods=['DELETE'])
def delete_amenity(id):
    """delete a amenity by its id"""
    amenity = storage.get(Amenity, id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return {}
    return abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """create a new amenity"""
    if request.is_json:
        data = request.get_json()
        if not data.get('name'):
            return 'Missing name', 400
        new_amenity = Amenity(**data)
        new_amenity.save()
        return new_amenity.to_dict(), 201

    return 'Not a JSON', 400


@app_views.route('amenities/<id>', methods=['PUT'])
def update_amenity(id):
    """update a amenity by its id"""
    amenity = storage.get(Amenity, id)
    if not amenity:
        return abort(404)
    if not request.is_json:
        return 'Not a JSON', 400
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    storage.save()
    return amenity.to_dict(), 200
