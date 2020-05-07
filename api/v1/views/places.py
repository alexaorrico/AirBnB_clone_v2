#!/usr/bin/python3
"""Routes for Place"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def showPlace(city_id):
    """ Shows all places in the file storage """
    count_l = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    eachPlace = storage.all("Place")
    for value in eachPlace.values():
        if value.city_id == city_id:
            count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET'])
def a_place_id(place_id):
    """ Gets the place and its id if any """
    i = storage.get("Place", place_id)
    if i:
        return jsonify(i.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=["DELETE"])
def del_place_id(place_id):
    """ deletes an place if given the id """
    thing = storage.all('Place')
    place = "Place." + place_id
    p = thing.get(place)
    if p is None:
        abort(404)
    else:
        p.delete()
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def postPlace(city_id):
    """ creates a new placee """
    if storage.get("City", city_id) is None:
        abort(404)
    thing = request.get_json()
    if not thing:
        return (jsonify({"error": "Not a JSON"}), 400)
    user = thing.get("user_id")
    if user is None:
        return (jsonify({"error": "Missing user_id"}), 400)
    useConfirm = storage.get("User", user)
    if useConfirm is None:
        abort(404)
    place = thing.get("name")
    if place is None:
        return (jsonify({"error": "Missing name"}), 400)
    p = Place()
    p.name = place
    p.city_id = city_id
    p.user_id = user
    p.save()
    return (jsonify(p.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=["PUT"])
def updatePlace(place_id):
    """ updates the place info, specifically name """
    # garbage = {"id", "created_at", "updated_at"}
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    thing = request.get_json()
    if not thing:
        return (jsonify({"error": "Not a JSON"}), 400)

    for key, value in thing.items():
        if key == 'name':
            setattr(place, key, value)
        if key == 'description':
            setattr(place, key, value)
        if key == 'number_rooms':
            setattr(place, key, value)
        if key == 'number_bathrooms':
            setattr(place, key, value)
        if key == 'max_guest':
            setattr(place, key, value)
        if key == 'price_by_night':
            setattr(place, key, value)
        if key == 'lattitude':
            setattr(place, key, value)
        if key == 'longitude':
            setattr(place, key, value)

    place.save()
    return (jsonify(place.to_dict()), 200)
