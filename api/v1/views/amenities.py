#!/usr/bin/python3
"""Amenities module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenities_id>',
                 methods=['GET'], strict_slashes=False)
def amenities(amenities_id=None):
    """
    Retrieves the list of all State objects or
    State objec from a rout
    """
    if amenities_id is None:
        st_all = []
        for st in storage.all(Amenity).values():
            st_all.append(st.to_dict())
        return jsonify(st_all)
    elif storage.get(Amenity, amenities_id):
        return jsonify(storage.get(Amenity, amenities_id).to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenities_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenities_id=None):
    """
    delete state if id is match with obj
    """
    if storage.get(Amenity, amenities_id):
        storage.delete(storage.get(Amenity, amenities_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def post_amenities():
    """
    arreglar
    """

    amen_dict = request.get_json()

    if amen_dict is None:
        abort(400, "Not a JSON")
    if "name" not in amen_dict.keys():
        abort(400, "Missing name")

    new_amenity = Amenity(**amen_dict)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenities_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenities(amenities_id=None):
    """
    arreglar
    """

    data = request.get_json()

    obj = storage.get(Amenity, amenities_id)

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
