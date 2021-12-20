#!/usr/bin/python3
""" Amenities routes handler """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


def check_id(cls, amenity_id):
    """
        check amenity
    """
    try:
        get_amenity = storage.get(cls, amenity_id)
        get_amenity.to_dict()
    except Exception:
        abort(404)
    return get_amenity


def get_amenities(amenity_id):
    """
       Retrieves the list of all Amenity objects
    """
    if (amenity_id is not None):
        get_amenity = check_id(Amenity, amenity_id).to_dict()
        return jsonify(get_amenity)
    all_amenities = storage.all(Amenity)
    amenities = []
    for v in all_amenities.values():
        amenities.append(v.to_dict())
    return jsonify(amenities)


def delete_amenity(amenity_id):
    """
        Deletes a Amenity object
    """
    get_amenity = check_id(Amenity, amenity_id)
    storage.delete(get_amenity)
    storage.save()
    response = {}
    return jsonify(response)


def create_amenity(request):
    """
        Creates a amenity object
    """
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    try:
        amenity_name = body_request['name']
    except KeyError:
        abort(400, 'Missing name')
    new_amenity = Amenity(name=amenity_name)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict())


def update_amenity(amenity_id, request):
    """
        Updates a Amenity object
    """
    get_amenity = check_id(Amenity, amenity_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    for k, v in body_request.items():
        if (k not in ('id', 'created_at', 'updated_at')):
            setattr(get_amenity, k, v)
    storage.save()
    return jsonify(get_amenity.to_dict())


@app_views.route('/amenities/', methods=['GET', 'POST'],
                 defaults={'amenity_id': None}, strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities(amenity_id):
    """
        Handle amenities requests
    """
    if (request.method == "GET"):
        return get_amenities(amenity_id)
    elif (request.method == "DELETE"):
        return delete_amenity(amenity_id)
    elif (request.method == "POST"):
        return create_amenity(request), 201
    elif (request.method == "PUT"):
        return update_amenity(amenity_id, request), 200
