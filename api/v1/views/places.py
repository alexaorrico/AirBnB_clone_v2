#!/usr/bin/python3
'''creates a new view for place objects'''
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def getter_places():
    '''getter_places - gets all Place objects'''
    new_list = []
    allplaces = list(storage.all("Place").values())

    for place in allplaces:
        new_list.append(place.to_dict())
    return jsonify(new_list)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def getter_places_id(city_id):
    '''getter_id - gets all Place objects by id'''
    new_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    allplaces = storage.all(Place).values()
    for object in allplaces:
        if object.city_id == city.id:
            new_list.append(object.to_dict())
    return jsonify(new_list)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def places_by_id(place_id):
    '''places_by_id - get places by place_id'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleter_places(place_id):
    '''deleter_id - delete an object by id'''
    id = storage.get(Place, place_id)

    if id is not None:
        storage.delete(id)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/city_id/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    '''post_place - create an place object with post'''
    if storage.get(City, city_id) is None:
        abort(404)
    if not request.get_json():
        return "Not a JSON", 400
    if "user_id" not in request.get_json():
        return "Missing user_id", 400
    #making request a variable to access it
    request = request.get_json()
    if storage.get(User, request["user_id"]) is None:
        abort(404)
    if "name" not in request:
        return "Missing name", 400
    request["city_id"] = city_id
    place = Place(**request)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    '''put_place - updates a place object by id'''
    placeId = storage.get(Place, place_id)

    if placeId is None:
        abort(404)
    body_dict = request.get_json()
    if body_dict is None:
        return "Not a JSON", 400
    body_dict.pop("id", None)
    body_dict.pop("created_at", None)
    body_dict.pop("updated_at", None)
    body_dict.pop("user_id", None)
    body_dict.pop("city_id", None)
    for key, value in body_dict.items():
        setattr(placeId, key, value)
    placeId.save()
    return jsonify(placeId.to_dict()), 200
