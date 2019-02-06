#!/usr/bin/python3
""" Amenities view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=[
                 'GET', 'PUT', 'DELETE'])
def all_amenities(amenity_id=None):
    """ retrieves all amenities """

    amenity_list = storage.all("Amenities").values()

    if amenity_id:
        try:
            amenity = storage.all("Amenities").pop("Amenity." + amenity_id)
        except KeyError:
            abort(404)

    if request.method == 'GET':
        if amenity_id is None:
            my_amenities = [amen.to_dict() for amen in amenity_list]
            return (jsonify(my_amenities))
        else:
            return (jsonify(amenity.to_dict()))

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return (jsonify({}), 200)

    data = request.get_json(silent=True)
    if data is None:
        return (jsonify({"error": 'Not a JSON'}), 400)

    if request.method == 'PUT':
        obj = storage.get("Amenity", amenity_id)
        if obj is None:
            abort(404)
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, k, v)
        amenity.save()
        return (jsonify(amenity.to_dict()), 200)

    if request.method == 'POST':
        if "name" not in data.keys():
            return (jsonify({"error": "Missing name"}), 400)
        amenity = Amenity(**data)
        amenity.save()
        return (jsonify(amenity.to_dict()), 201)
