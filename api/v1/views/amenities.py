#!/usr/bin/python3
"""new view for Amenity objects that handles all default RESTFul API"""
from models import storage, amenity
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'])
def listallamenity():
    """list of all Amenity objects"""
    temp = []
    for i in storage.all("Amenity").values():
        temp.append(j.to_dict())

    return (temp)

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def deleteamenity(amenity_id=None):
    """Deletes a Amenity object"""
    a = storage.get("Amenity", amenity_id)
    if a is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'])
def createamenity():
    """Creates a Amenity"""
    a = storage.request.get_json("Amenity", silent=True)
    if a == None:
        return (400, "Not a JSON")
    elif "name" not in  a.keys():
        return (400, "Missing name")
    else:
        return (jsonify({}), 201)

@app_views.route('/amenities/<amenity_id>', method=['PUT'])
def updateamenity(amenity_id=None):
    """Updates a Amenity object"""
    am = storage.get("Amenity", amenity_id)
    if am is None:
        abort(404)
    a = storage.request.get_json("Amenity", silent=True)
    elif a == None:
        abort(400, "Not a JSON")
