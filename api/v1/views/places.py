#!/usr/bin/python3
"""restful API functions for City"""
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import request, jsonify, abort


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=["GET", "POST"]
                 )
def cities_end_points(city_id):
    """city objects that handles all default RESTFul API actions"""
    obj_cities = storage.all(City)
    cities_dict = [obj.to_dict() for obj in obj_cities.values()]
    if request.method == "GET":
        for obj in cities_dict:
            if obj.get('id') == city_id:
                obj_places = storage.all(Place)
                places_dict = [obj.to_dict() for obj in
                               obj_places.values() if
                               obj.city_id == city_id]
                return jsonify(places_dict)
        abort(404)

    elif request.method == "POST":
        for obj in cities_dict:
            if obj.get('id') == city_id:
                my_dict = request.get_json()
                if not my_dict or type(my_dict) is not dict:
                    abort(400, "Not a JSON")
                if not my_dict["name"]:
                    abort(400, "Missing name")
                if not my_dict.get('user_id'):
                    abort(400, "Missing user_id")
                user_obj = storage.all(User).values()
                user_exists = False
                for user_obj in user_objs:
                    if user_obj.id == my_dict["user_id"]:
                        user_exists = True
                        break
                if not user_exists:
                    abort(404)
                else:
                    my_dict["city_id"] = city_id
                    new_place = Place(**my_dict)
                    new_place.save()
                    return jsonify(new_place.to_dict()), 201
        abort(404)


@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=["DELETE", "PUT", "GET"])
def place_end_points(place_id):
    """city objects that handles all default RESTFul API actions"""
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    if request.method == "GET":
        return jsonify(obj_place.to_dict())
    elif request.method == "DELETE":
        storage.delete(obj_place)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        get_new_name = request.get_json()
        if not get_new_name or type(get_new_name) is not dict:
            abort(400, "Not a JSON")
        obj_placename = get_new_name.get("name")
        obj_place.save()
        return jsonify(obj_place.to_dict()), 200
