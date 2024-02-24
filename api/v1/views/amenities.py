#!/usr/bin/python3
"""api amenities"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
import json


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """retrieves all amenities"""
    allAmenities = storage.all(Amenity).values()
    amenitiesList = []
    for amenity in allAmenities:
        amenitiesList.append(amenity.to_dict())
    response = make_response(json.dumps(amenitiesList), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<id>", methods=["GET"])
def get_amenity(id):
    """retrieves amenity object with id"""
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    response_data = amenity.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<id>", methods=["DELETE"])
def delete_amenity(id):
    """delets amenity with id"""
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """inserts amenities if its valid json"""
    abortMSG = "Not a JSON"
    missingMSG = "Missing name"
    if not request.get_json():
        abort(400, description=abortMSG)
    if "name" not in request.get_json():
        abort(400, description=missingMSG)
    data = request.get_json()
    instObj = Amenity(**data)
    instObj.save()
    res = instObj.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<id>", methods=["PUT"])
def put_amenity(id):
    """update a amenities by id"""
    abortMSG = "Not a JSON"
    amenity = storage.get(Amenity, id)
    ignoreKeys = ["id", "created_at", "updated_at"]
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(amenity, key, value)
    storage.save()
    res = amenity.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response
