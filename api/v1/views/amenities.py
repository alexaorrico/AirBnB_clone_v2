#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity

@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get():
    result = []
    """ get all the amenity """
    for i in storage.all("Amenity").values():
        result.append(i.to_dict())
    return jsonify(result)


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def amenity_specific(amenity_id):
    """ get the specific object from amenity """
    for i in storage.all("Amenity").values():
        if i.id == amenity_id:
            return i.to_dict()
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
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


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def postAmenity():
    """ creates a new Amenity """
    thing = request.get_json()
    if thing is None or not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    amenity = thing.get("name")
    if amenity is None or len(thing) == 0:
        return (jsonify({"error": "Missing name"}), 400)
    try:
        a = Amenity()
        a.name = amenity
        a.save()
        return (jsonify(a.to_dict()), 201)
    except BaseException:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def amenity_specific_put(amenity_id):
    """ update the specific object from amenity """
    instance = None
    if not request.json:
        return make_response("Not a JSON", 400)
    check = ["id", "created_at", "updated_at"]
    for i in storage.all("Amenity").values():
        if i.id == amenity_id:
            instance = i
            for key, value in request.json.items():
                if key not in check:
                    setattr(i, key, value)
                    i.save()
    if not instance:
        abort(404)
    return instance.to_dict(), 200