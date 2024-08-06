#!/usr/bin/python3


"""  TODO: Doc """


from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ TODO: Doc"""
    amenities_dicts = storage.all(Amenity)
    array_of_objs = []
    for value in amenities_dicts.values():
        array_of_objs.append(value.to_dict())
    return jsonify(array_of_objs)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenit_ById(amenity_id):
    """  TODO: Doc """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404, description="Amenity not found")
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """  TODO: Doc """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404, description="Amenity not found")
    try:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500, description="Error while deleting")


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """  TODO: Doc """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404, description="Amenity not found")
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    bad_keys = ['id', 'created_at', 'updated_at']
    for key in data.keys():
        if key not in bad_keys:
            setattr(amenity_obj, key, data[key])
        amenity_obj.save()
        return jsonify(amenity_obj.to_dict()), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """  TODO: Doc """
    if request.is_json:
        data = request.get_json()
        if 'name' not in data:
            abort(400, description="Missing name")
        else:
            amenity_obj = Amenity(**data)
            amenity_obj.save()
            return jsonify(amenity_obj.to_dict()), 201
    else:
        abort(400, description="Not a JSON")
