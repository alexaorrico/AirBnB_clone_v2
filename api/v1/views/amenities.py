#!/usr/bin/python3
"""handling Amenity objects and operations"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """retrieves all Amenity objects"""
    list_ems = []
    objs = storage.all("Amenity")
    for obj in objs.values():
        list_ems.append(obj.to_dict())
    return jsonify(list_ems)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """create amenity route"""
    json_ems = request.get_json(silent=True)
    if json_ems is None:
        abort(400, 'Not a JSON')
    if "name" not in json_ems:
        abort(400, 'Missing name')
    new_amenity = Amenity(**json_ems)
    new_amenity.save()
    response = jsonify(new_amenity.to_dict())
    response.status_code = 201
    return response


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """gets a specific Amenity object by ID
    Args:
        amenity_id: amenity object id"""
    objs = storage.get("Amenity", str(amenity_id))
    if objs is None:
        abort(404)
    return jsonify(objs.to_dict())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """updates specific Amenity object by ID
    Args:
        amenity_id: amenity object ID"""
    json_ems = request.get_json(silent=True)
    if json_ems is None:
        abort(400, 'Not a JSON')
    objs = storage.get("Amenity", str(amenity_id))
    if objs is None:
        abort(404)
    for key, val in json_ems.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(objs, key, val)
    objs.save()
    return jsonify(objs.to_dict())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """deletes Amenity by id
    Args:
        amenity_id: Amenity object id"""
    objs = storage.get("Amenity", str(amenity_id))
    if objs is None:
        abort(404)
    storage.delete(objs)
    storage.save()
    return jsonify({})
