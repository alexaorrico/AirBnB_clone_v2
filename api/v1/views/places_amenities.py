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
    @app_views.route("/places/<place_id>/amenities", strict_slashes=False)
    def get_list_amenities_db(place_id):
        """
        retrieves the list of all Amenity objects of a Place
        """
        list_obj = []
        place_obj = storage.get("Place", place_id)
        if place_obj:
            print("--------- {} -------".format(place_obj.amenities))
            for amenity in place_obj.amenities:
                print("======== {} ========".format(amenity))
                list_obj.append(amenity.to_dict())
            return jsonify(list_obj)
        else:
            abort(404)

    @app_views.route("/places/<place_id>/amenities/<amenity_id>",
                     methods=["DELETE"], strict_slashes=False)
    def delete_amenity_db(place_id, amenity_id):
        """
        deletes a Amenity object to a Place
        """
        list_obj = []
        place_obj = storage.get("Place", place_id)
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj is None or place_obj is None:
            abort(404)
        if not place_id or not amenity_id:
            abort(404)
        for amenity in place_obj.amenities:
            amenity_dic_obj = amenity.to_dict()
            if amenity_dic_obj["id"] == amenity_id:
                storage.delete(amenity)
                storage.save()
        if amenity is None:
            abort(404)
        else:
            return jsonify({})


    @app_views.route("/places/<place_id>/amenities/<amenity_id>",
                     methods=["POST"], strict_slashes=False)
    def post_place_amenity(place_id, amenity_id):
        """
        link a Amenity object to a Place
        """
        place_obj = storage.get("Place", place_id)
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj is None or place_obj is None:
            abort(404)
        for amenity in place_obj.amenities:
            amenity_dict_obj = amenity.to_dict()
            if amenity_dict_obj["id"] == amenity_id:
                return jsonify(amenity_dict_obj)
        place_obj.amenities.append(amenity_obj)
        storage.save()
        return (jsonify(amenity_obj.to_dict()), 201)

else:
    @app_views.route("/places/<place_id>/amenities", strict_slashes=False)
    def get_list_amenities_fl(place_id):
        """
        retrieves the list of all Amenity objects of a Place
        """
        place_obj = storage.get("Place", place_id)
        if place_obj:
            jsonify(place_obj.amenities())
        else:
            abort(404)

    @app_views.route("/places/<place_id>/amenities/<amenity_id>",
                     methods=["DELETE"], strict_slashes=False)
    def delete_amenity_fl(place_id, amenity_id):
        """
        deletes a Amenity object to a Place
        """
        list_obj = []
        place_obj = storage.get("Place", place_id)
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj is None or place_obj is None:
            abort(404)
        if not place_id or not amenity_id:
            abort(404)
        for amenity in place_obj.amenities():
            amenity_dic_obj = amenity.to_dict()
            if amenity_dic_obj["id"] == amenity_id:
                storage.delete(amenity.id)
                storage.save()
        if amenity is None:
            abort(404)
        else:
            return jsonify({})


    @app_views.route("/places/<place_id>/amenities/<amenity_id>",
                     methods=["POST"], strict_slashes=False)
    def post_place_amenity_fl(place_id, amenity_id):
        """
        link a Amenity object to a Place
        """
        place_obj = storage.get("Place", place_id)
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj is None or place_obj is None:
            abort(404)
        for amenity in place_obj.amenities():
            amenity_dict_obj = amenity.to_dict()
            if amenity_dict_obj["id"] == amenity_id:
                return jsonify(amenity_dict_obj)
        storage.append(amenity.id)
        storage.save()
        return (jsonify(amenity_obj.to_dict()), 201)
