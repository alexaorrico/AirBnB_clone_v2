#!/usr/bin/python3
"""States views"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def view_amenities():
    """Returns the list of all Amenity objects"""
    if request.method == 'POST':

        # Get the attributes from the request
        data = request.get_json()

        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        if 'name' not in data.keys():
            return jsonify({'error': 'Missing name'}), 400

        if 'id' in data.keys():
            data.pop("id")
        if 'created_at' in data.keys():
            data.pop("created_at")
        if 'updated_at' in data.keys():
            data.pop("updated_at")

        # Create the object
        obj = Amenity(**data)

        # Save the object in storage
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201

    if request.method == 'GET':
        amenities = storage.all("Amenity")
        list = []
        for name, amenity_obj in amenities.items():
            list.append(amenity_obj.to_dict())
        return jsonify(list)


@app_views.route('/amenities/<id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def view_amenity(id):
    """Returns a list of all Amenity objects, or delete an
    object if a given id
    """
    amenity = storage.get(Amenity, id)

    if amenity is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()

        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)

        storage.save()
        return jsonify(amenity.to_dict())
