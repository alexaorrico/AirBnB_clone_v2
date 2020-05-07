#!/usr/bin/python3
"""Routes for Amenities"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def showAmenity():
    """ Shows all amenities in the file storage """
    count_l = []
    for value in storage.all("Amenity").values():
        count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET'])
def a_amenity_id(amenity_id):
    """ Gets the amenity and its id if any """
    i = storage.get("Amenity", amenity_id)
    if i:
        return jsonify(i.to_dict())
    else:
        return (jsonify({"error": "Not found"}), 404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_amenity_id(amenity_id):
    """ deletes an amenity if given the id """
    thing = storage.all('Amenity')
    ameny = "Amenity." + amenity_id
    amens = thing.get(ameny)
    if amens is None:
        abort(404)
    else:
        amens.delete()
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def postAmenity():
    """ creates a new Amenity """
    thing = request.get_json()
    if thing is None or not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    amenity = thing.get("name")
    if amenity is None or len(thing) == 0:
        return (jsonify({"error": "Missing name"}), 400)
    a = Amenity()
    a.name = amenity
    a.save()
    return (jsonify(a.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def updateAmenity(amenity_id):
    """ updates the amenity info, specifically name """
    # garbage = {"id", "created_at", "updated_at"}
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    thing = request.get_json()
    for key, value in thing.items():
        if key == 'name':
            setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
