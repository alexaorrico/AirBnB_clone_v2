#!/usr/bin/python3
"""amenities al7bin"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from json import dumps


def json_ser(obj):
    json_obj = {}
    for key in obj:
        json_obj[key] = obj[key].to_dict()
    return (json_obj)


def cities_json(lst):
    json_list = []
    for city in lst:
        json_list.append(city.to_dict())
    return (json_list)


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    return make_response(
        dumps(list(json_ser(storage.all(Amenity)).values())),
        200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    return (amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(({}), 200)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return make_response((amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key in data:
        if key in ['id', 'created_at', 'updated_at']:
            continue
        value = data[key]
        if hasattr(amenity, key):
            try:
                value = type(getattr(amenity, key))(value)
            except ValueError:
                pass
        setattr(amenity, key, value)
    storage.save()
    return make_response(amenity.to_dict(), 200)
