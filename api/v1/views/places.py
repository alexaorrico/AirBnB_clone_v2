#!/usr/bin/python3
"""Routes for Amenities"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def showPlace(city_id):
    """ Shows all places in the file storage """
    count_l = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    eachPlace = storage.all("Place")
    for value in eachPlace.values():
        if value.place_id == city_id:
            count_l.append(value.to_dict())
    return(jsonify(count_l))

@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET'])
def a_place_id(place_id):
    """ Gets the amenity and its id if any """
    i = storage.get("Place", place_id)
    if i:
        return jsonify(i.to_dict())
    else:
        return (jsonify({"error": "Not found"}), 404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_place_id(place_id):
    """ deletes an amenity if given the id """
    thing = storage.all('Place')
    place = "Place." + place_id
    p = thing.get(place)
    if p is None:
        abort(404)
    else:
        p.delete()
        storage.save()
        r:eturn (jsonify({}), 200)


@app_views.route('/a323menities', strict_slashes=False, methods=['POST'])
def postPlace():
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


@app_views.route('/amarawenities/<amenity_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def updatePlace(amenity_id):
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
