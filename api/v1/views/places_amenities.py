#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.amenity import Amenity
import json
import models

@app_views.route("/places/<place_id>/amenities/", methods=['GET'])
@app_views.route("/places/<place_id>/amenities", methods=['GET'])
def show_place_amenities(place_id):
    """ returns list of amenities from place """
    if models.storage_t == 'db':
        if request.method == 'GET':
            places = storage.get(Place, place_id)
            if places:
                lista = []
                for amenity in places.amenities:
                    lista.append(amenity.to_dict())
                return jsonify(lista)
            abort(404)
    else:
        if request.method == 'GET':
            places = storage.get(Place, place_id)
            if place:
                lista = []
                for amenity in places.amenity_ids:
                    lista.append(amenity.to_dict())
                return jsonify(lista)
            abort(404)

@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['DELETE', 'POST'])
@app_views.route("/places/<place_id>/amenities/<amenity_id>/", methods=['DELETE', 'POST'])
def show_place_amenity(place_id, amenity_id):
    """ returns amenity data from place """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if request.method == 'DELETE':
            for amenit in place.amenities:
                if amenit.id == amenity_id:
                    new_dict = {}
                    amenit.delete()
                    storage.save()
                    return jsonify(amenit.to_dict()), 200
        elif request.method == 'POST':
            for amenit in place.amenities:
                if amenit.id == amenity_id:
                    return jsonify(amenit.to_dict()), 200
            setattr(place, 'amenity_id', amenity_id)
            return jsonify(amenit.to_dict()), 201
    abort(404)
