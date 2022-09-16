#!/usr/bin/python3
"""view for amenities"""


from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """return list of all objects Amenity"""
    new_list = list()
    lst_amenities = storage.all('Amenity')
    for value in lst_amenities.values():
        new_list.append(value.to_dict())
    return jsonify(new_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity_id(amenity_id):
    """Return dictionary of specific amenity"""
    ret = storage.get("Amenity", amenity_id)
    if ret:
        return ret.to_dict()
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an specific Amenity"""
    ret = storage.get('Amenity', amenity_id)
    if ret:
        storage.delete(ret)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Create a new amenity"""
    from models.amenity import Amenity
    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")
    name_amenity = content.get('name')
    if "name" not in content.keys():
        abort(400, "Missing name")

    new_instance = Amenity(name=name_amenity)
    return jsonify(new_instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """Update a amenity by a given ID"""
    new_amenity = storage.get('Amenity', amenity_id)
    if not new_amenity:
        abort(404)

    content = request.get_json(force=True, silent=True)
    if not content:
        abort(400, "Not a JSON")

    to_ignore = ['id', 'created_at', 'update_at']
    for key, value in content.items():
        if key in to_ignore:
            continue
        else:
            setattr(new_amenity, key, value)
    storage.save()
    return jsonify(new_amenity.to_dict()), 200
