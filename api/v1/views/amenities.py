#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Amenity objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from model.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities()
""" retrieves the list of all Amenity objects """
amenities_list = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
return jsonify(amenities_list)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ retrieves a Amenity object """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

        amenity_dict = amenity_obj.to_dict()
        return jsonify(amenity_dict)

    @app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
    def delete_amenity(amenity_id):
        """ delete an/a Amenity object"""
        amenity_obj = storage.get(Amenity, amenity_id)
        if amenity_obj is None:
            abort(404)

            storage.delete(amenity_obj)
            storage.save()
            return jsonify({}), 200


        @app_views.route('/amenities', methods=['POST'], strict_slashes=False)
        def create_amenity():
            """ Create an/a amenity object"""
            json_data = request.get_json()
            if json_data is None:
                return jsonify({"error": "Not a JSON"}), 400
            elif 'name' not in json_data.keys():
                return jsonify({"error": "Missing name"}), 400

            new_obj = Amenity(**json_data)
            new_obj.save()

            return jsonify(new_obj.to_dict()), 201

        @app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
        def update_amenity(amenity_id):
            """ updates an/a Amenity object"""
            amenity_obj = storage.get(Amenity, amenity_id)
            if amenity_obj is None:
                abort(404)

                json_data = request.get_json()
                if json_data is None:
                    return jsonify({"error": "Not a JSON"}), 400
                for attr, val in json_data.items():
                    if attr not in ['id', 'created_at', 'updated_at']:
                        setattr(amenity_obj, attr, val)
                        amenity_obj.save()

                        return jsonify(amenity_obj.to_dict()), 200
