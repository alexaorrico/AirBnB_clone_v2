#!/usr/bin/python3
"""amenities view module"""
from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """returns list of all amenities"""
    if request.method == 'GET':
        amenities_list = []
        for amenity, value in storage.all(Amenity).items():
            amenity = value.to_dict()
            amenities_list.append(amenity)
        return jsonify(amenities_list)

    if request.method == 'POST':
        # If not valid JSON, error 400
        try:
            request_data = request.get_json()
            if 'name' not in request_data:
                abort(400, "Missing name")
            newamenity = Amenity(**request_data)
            newamenity.save()
        except Exception:
            abort(400, "Not a JSON")
        return jsonify(newamenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_search(amenity_id):
    """returns amenity with id or 404"""
    amenity = storage.get(Amenity, amenity_id)
    #  If GET
    if request.method == 'GET':
        for amenity, value in storage.all(Amenity).items():
            id = (amenity.split(".")[1])
            if amenity_id == id:
                return jsonify(value.to_dict())
        abort(404)

    #  If DELETE
    if request.method == 'DELETE':
        if amenity is None:
            abort(404)
        amenity.delete()
        storage.save()
        return {}

    # If PUT
    if request.method == 'PUT':
        # If not valid JSON, error 400
        if amenity is None:
            abort(404)
        try:
            request_data = request.get_json()
            for amenity, value in storage.all(Amenity).items():
                id = (amenity.split(".")[1])
                if amenity_id == id:
                    for k in request_data.keys():
                        if k != 'id' and\
                                k != 'created_at' and k != 'updated_at':
                            setattr(value, k, request_data[k])
                    storage.save()
                return jsonify(value.to_dict())
        except Exception:
            abort(400, "Not a JSON")
        abort(404)
