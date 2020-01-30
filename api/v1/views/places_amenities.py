#!/usr/bin/python3
"""
File that add a new view for linking Place and Amenity
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import *
from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")


if storage_t == "db":
    @app_views.route("/places/<place_id>/amenities")
    def get_list_amenities_db(place_id):
        list_obj = []
        place_amenity_obj = storage.get("Place", place_id).amenities

        if place_amenity_obj:
            for i in place_amenity_obj:
                list_obj.append(i.to_dict())
            return jsonify(list_obj)
        else:
            abort(404)

    @app_views.route("/places/<place_id>/amenities/<amenity_id>",
                     methods=["DELETE"], strict_slashes=False)
    def delete_amenity_db(place_id, amenity_id):
        if not place_id or not amenity_id:
            abort(404)

        place_amenity_obj = storage.get("Place", place_id).amenities

        a = None
        if place_amenity_obj:
            for i in place_amenity_obj:
                dic_obj = i.to_dict()
                if dic_obj["id"] == amenity_id:
                    storage.delete(i)
                    storage.save()
                    obj_amenity = i
            if obj_amenity is None:
                abort(404)
            else:
                return jsonify({})
        else:
            abort(404)

    @app_views.route("/places/<place_id>/amenities/<amenity_id>",
                     methods=["POST"], strict_slashes=False)
    def post_place_amenity(place_id, amenity_id):
        place_obj = storage.get("Place", place_id)
        amenity_obj = storage.get("Amenity", amenity_id)

        for i in place_obj.amenities:
            i = i.to_dict()
            if i["id"] == amenity_id:
                return jsonify(i)

        if place_obj is None:
            abort(404)
        if amenity_obj is None:
            abort(404)

        place_obj.amenities.append(amenity_obj)
        storage.save()
        return jsonify(amenity_obj.to_dict())


else:
    @app_views.route("/places/<place_id>/amenities")
    def get_list_amenities_fs(place_id):
        list_obj = []
        place_amenity_obj = storage.get("Place", place_id).amenities

        if place_amenity_obj:
            for i in place_amenity_obj:
                list_obj.append(i.to_dict())
            return jsonify(list_obj)
        else:
            abort(404)

    @app_views.route("/places/<place_id>/amenities/<amenity_id>",
                     methods=["DELETE"], strict_slashes=False)
    def delete_amenity_db(place_id, amenity_id):
        if not place_id or not amenity_id:
            abort(404)

        place_amenity_obj = storage.get("Place", place_id).amenities

        a = None
        if place_amenity_obj:
            for i in place_amenity_obj:
                dic_obj = i.to_dict()
                if dic_obj["id"] == amenity_id:
                    storage.delete(i)
                    storage.save()
                    obj_amenity = i
            if obj_amenity is None:
                abort(404)
            else:
                return jsonify({})
        else:
            abort(404)

    @app_views.route("/places/<place_id>/amenities/<amenity_id>",
                     methods=["POST"], strict_slashes=False)
    def post_place_amenity(place_id, amenity_id):
        place_obj = storage.get("Place", place_id)
        amenity_obj = storage.get("Amenity", amenity_id)

        for i in place_obj.amenities:
            i = i.to_dict()
            if i["id"] == amenity_id:
                return jsonify(i)

        if place_obj is None:
            abort(404)
        if amenity_obj is None:
            abort(404)

        place_obj.amenities.append(amenity_obj)
        storage.save()
        return jsonify(amenity_obj.to_dict())
