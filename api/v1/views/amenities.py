#!/usr/bin/python3
"""amenities"""
from models import storage
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrieve_amenities():
    """retrieve a list of amenities by id"""
    list_of_amenities = storage.all(Amenity).values()
    display = [amenity.to_dict() for amenity in list_of_amenities]
    return jsonify(display)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'], strict_slashes=False)
def retrieve_obj(amenity_id):
    """return amenity object"""
    obj_id = storage.get(Amenity, amenity_id)
    if (obj_id is None):
        abort(404)
    return jsonify(obj_id.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def delete(amenity_id=None):
    """delete from list of states"""
    deleted = storage.get(Amenity, amenity_id)
    if deleted is None:
        abort(404)
    else:
        storage.delete(deleted)
        storage.save()
        return (jsonify({}), 200)


@app_views.route("/amenities/<amenity_id>", methods=['POST'], strict_slashes=False)
def create():
    """create new amenity from list"""
    new_amenity = request.get_json()
    if new_amenity is None:
        return (jsonify({'Error': 'Not a JSON'}), 400)
    if 'name' not in new_amenity.key():
        return (jsonify({'Error': 'Missing name'}), 400)
    amenity = Amenity(**new_amenity)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update(amenity_id=None):
    """update my amenity"""
    update_amenity = request.get_json()
    if update_amenity is None:
        return jsonify({'Error': 'Not a JSON'}), 400
    new_amenity = storage.get(Amenity, amenity_id)
    if new_amenity is None:
        abort(404)
    else:
        keys = ['id', 'created_at', 'updated_at']
        for key, value in update_amenity.items():
            if key not in keys:
                setattr(new_amenity, key, value)
            else:
                pass
        new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 200)

