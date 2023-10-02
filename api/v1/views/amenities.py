#!/usr/bin/python3
""" route amenities """
from flask import request, abort, jsonify
from api.v1.app import *
from api.v1.views import *
from models import storage, Amenity


def validate(cls, ref_id):
    """ validate if query have id to reference """
    try:
        valid = storage.get(cls, ref_id)
        valid.to_dict()
    except Exception:
        abort(404)
    return valid


def get_amenities(amenity_id):
    """ list of amenities """
    if (amenity_id is not None):
        get_amenity = validate(Amenity, amenity_id).to_dict()
        return jsonify(get_amenity)
    amenity_obj = storage.all(Amenity)
    amenities = []
    for amenity in amenity_obj.values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


def delete_amenity(amenity_id):
    """ delete amenitie by id """
    amenity = validate(Amenity, amenity_id)
    storage.delete(amenity)
    storage.save()
    response = {}
    return jsonify(response)


def create_amenity(request):
    """ create amenity """
    request_json = request.get_json()
    if (request_json is None):
        abort(400, 'Not a JSON')
    try:
        amenity_name = request_json['name']
    except KeyError:
        abort(400, "Missing name")
    new_amenity = Amenity(name=amenity_name)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict())


def update_amenity(amenity_id, request):
    """ updates amenity """
    get_amenity = validate(Amenity, amenity_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    for key, value in body_request.items():
        if (key not in ('id', 'created_at', 'updated_at')):
            setattr(get_amenity, key, value)
    storage.save()
    return jsonify(get_amenity.to_dict())


@app_views.route('/amenities/', methods=['GET', 'POST'],
                 defaults={'amenity_id': None}, strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def amenities(amenity_id):
    """ Switch routes """
    if (request.method == "GET"):
        return get_amenities(amenity_id)
    elif (request.method == "DELETE"):
        return delete_amenity(amenity_id)
    elif (request.method == "POST"):
        return create_amenity(request), 201
    elif (request.method == "PUT"):
        return update_amenity(amenity_id, request), 200