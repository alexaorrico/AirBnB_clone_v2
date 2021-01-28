#!/usr/bin/python3
""" Module cities """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_getstate(state_id=None):
    """Retrieve list amenity objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_amenities = []
    for i in state.amenities:
        list_amenities.append(i.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id=None):
    """get amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Delete Amenity"""
    if storage.get(Amenity, amenity_id):
        storage.delete(storage.get(Amenity, amenity_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity(state_id):
    """ post method """
    if storage.get(State, state_id) is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif "name" not in data.keys():
        abort(400, "Missing name")
    else:
        new_ame = Amenity(**data)
        storage.save()
    return jsonify(new_ame.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id=None):
    """Put method"""
    data = request.get_json()
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    if data is None:
        return "Not a JSON", 400
    for k, v in data.items():
        if k in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
