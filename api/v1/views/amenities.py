#!/usr/bin/python3
""" handles all default RESTFul API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities_all():
    """Retrieves the list of all Amenity objects """
    amenity_l = []
    amenity_o = storage.all("Amenity")
    for obj in amenity_o.values():
        amenity_l.append(obj.to_dict())

    return jsonify(amenity_l)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """Deletes a Amenity object"""
    d_obj = storage.get("Amenity", str(amenity_id))
    if d_obj is None:
        abort(404)

    storage.delete(d_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """Creates a Amenity"""
    amenity_j = request.get_json(silent=True)
    if amenity_j is None:
        abort(400, description='Not a JSON')
    if "name" not in amenity_j:
        abort(400, description='Missing name')

    new_amenity = Amenity(**amenity_j)
    new_amenity.save()
    repo = jsonify(new_amenity.to_dict())
    repo.status_code = 201

    return repo


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """update a amenity"""
    amenity_j = request.get_json(silent=True)
    if amenity_j is None:
        abort(400, 'Not a JSON')
    d_obj = storage.get("Amenity", str(amenity_id))
    if d_obj is None:
        abort(404)
    for key, val in amenity_j.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(d_obj, key, val)
    d_obj.save()
    return jsonify(d_obj.to_dict())
