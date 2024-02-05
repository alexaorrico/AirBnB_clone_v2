#!/usr/bin/python3
""" This module contains a blue print for a restful API that
    works for place objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


@app_views.route(
        '/places/<place_id>/amenities',
        methods=['GET'], strict_slashes=False
        )
def get_amenity_obj(place_id):
    """ This function contains two http method handler

        GET:
            return the all amenity objects related to the place_id
        POST:
            create a new amenity with the city_id given
        """
    if request.method == 'GET':
        place_objects = storage.all(Place)
        key = f'Place.{place_id}'
        place = place_objects.get(key)
        amenity_list = []
        if place:
            if os.getenv("HBNB_TYPE_STORAGE") == "db":
                for amenity in place.amenities:
                    amenity_list.append(amenity.to_dict())
            else:
                amenities = storage.all(Amenity)
                for amenity_id in place.amenity_ids:
                    key = f'Amenity.{amenity_id}'
                    amenity = amenities.get(key)
                    if amenity:
                        amenity_list.append(amenity.to_dict())
            return jsonify(amenity_list)
        else:
            abort(404)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST', 'DELETE'], strict_slashes=False
        )
def post_amenity_obj(place_id, amenity_id):
    """ This function contains two http method handler

        DELETE:
            delete an amenity with the respective amenity_id
            attached to the place

        POST:
            create a new amenity with the place_id given
        """
    place_objects = storage.all(Place)
    key = f'Place.{place_id}'
    place = place_objects.get(key)
    if not place:
        abort(404)
    amenity_objects = storage.all(Amenity)
    key = f'Amenity.{amenity_id}'
    amenity = amenity_objects.get(key)
    if not amenity:
        abort(404)
    if request.method == 'POST':
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)
                place.save()
                return jsonify(amenity.to_dict()), 201
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amentiy_ids.append(amenity_id)
                place.save()
                return jsonify(amenity.to_dict()), 201
    elif request.method == 'DELETE':
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
            return jsonify({}), 200
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)
            return jsonify({}), 200
