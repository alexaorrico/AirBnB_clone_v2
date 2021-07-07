#!/usr/bin/python3
"""view of State object"""
from api.v1.views import app_views
from models import storage, place, city, user
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=["GET"])
def place_ret(city_id):
    """return json Place objects"""
    place_list = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=["GET"])
def place_get_by_id(place_id):
    """return json Place objects by id"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=["DELETE"])
def place_delete(place_id=None):
    """delete an object by id"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places_search', methods=["POST"])
def search_place():
    """search place"""
    dic = {}
    all_objs = []
    list_city_id = []
    ret_list = []
    dic = request.get_json(silent=True)

    if dic is None:
        """If not JSON, rais 400 error with message
        Not a JSON"""
        abort(400, "Not a JSON")
    all_places = storage.all("Place")

    if dic == {}:
        """if empty, return all place objects
        """
        for value in all_places.values():
            all_objs.append(value.to_dict())
        return jsonify(all_objs), 201
    all_cities = storage.all("City")

    if "states" in dic.keys() and dic["states"] != []:
        """if states list not empty, all place linked to
        state id"""
        for state_obj_id in dic["states"]:
            state_obj = storage.get("State", state_obj_id)
            for city_obj in state_obj.cities:
                list_city_id.append(city_obj.id)

    if "cities" in dic.keys() and dic["cities"] != []:
        """if cities not empty, narrow the list by
        city_id"""
        for p in all_places.values():
            if (p.city_id in dic["cities"] or p.city_id in list_city_id):
                all_objs.append(p)
                
    if all_objs == []:
        """if states and cities are empty, retrieve all places
        """
        all_objs = list(all_places.values())

    if "amenities" in dic.keys() and dic["amenities"] != []:
        for place_obj in all_objs:
            ret_list.append(place_obj.to_dict())
            place_list_amenities = []
            for amenity in place_obj.amenities:
                place_list_amenities.append(amenity.id)
            if set(dic["amenities"]) > set(place_list_amenities):
                ret_list.pop()
        return jsonify(ret_list), 201
    else:
        for value in all_objs:
            ret_list.append(value.to_dict())
        return jsonify(ret_list), 201


@app_views.route('/cities/<city_id>/places', methods=["POST"])
def post_place_obj(city_id):
    """add new place object"""
    dic = {}
    if storage.get("City", city_id) is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    if "user_id" not in dic.keys():
        abort(400, "Missing user_id")
    if storage.get("User", dic["user_id"]) is None:
        abort(404)
    if "name" not in dic.keys():
        abort(400, "Missing name")
    new_place = place.Place()
    setattr(new_place, "city_id", city_id)
    for k, v in dic.items():
        setattr(new_place, k, v)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"])
def update_place_obj(place_id=None):
    """update new state object"""
    dic = {}
    list_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        if key not in list_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
