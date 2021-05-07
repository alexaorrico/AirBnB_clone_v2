#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
import json

@app_views.route("/amenities/", methods=['GET', 'POST'])
@app_views.route("/amenities", methods=['GET', 'POST'])
def show_amenities():
    """ returns list of states """
    if request.method == 'GET':
        lista = []
        amenities = storage.all(Amenity).values()
        for amenity in amenities:
            lista.append(amenity.to_dict())
        return jsonify(lista)
    elif request.method == 'POST':
        if request.json:
            new_dict = request.get_json()
            if "name" in new_dict.keys():
                new_amenity = Amenity(**new_dict)
                storage.new(new_amenity)
                storage.save()
                return jsonify(new_amenity.to_dict()), 201
            else:
                abort(400, description="Missing name")
        else:
            abort(400, description="Not a JSON")

@app_views.route("amenities/<amenity_id>/", methods=['GET', 'DELETE', 'PUT'])
@app_views.route("amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'])
def show_amenity(amenity_id):
    """ returns state data """
    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        for amenity in amenities:
            if amenity.id == amenity_id:
                return jsonify(amenity.to_dict())
        abort(404)
    elif request.method == 'DELETE':
        amenities = storage.all(Amenity).values()
        for amenity in amenities:
            if amenity.id == amenity_id:
                amenity.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)
    elif request.method == 'PUT':
        if request.json:
            new_dict = request.get_json()
            amenities = storage.all(Amenity).values()
            for amenity in amenities:
                if amenity.id == amenity_id:
                    amenity.name = new_dict['name']
                    storage.save()
                    return jsonify(amenity.to_dict()), 200
            abort(404)
        else:
            abort(400, description="Not a JSON")
