#!/usr/bin/python3
"""Places module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False)
@app_views.route(
    '/places/<place_id>',
    methods=['GET'],
    strict_slashes=False)
def placeof_city(city_id=None, place_id=None):
    if place_id:
        obj_place = storage.get(Place, place_id)
        if obj_place:
            return jsonify(obj_place.to_dict())
        else:
            abort(404)

    if city_id:
        acity = storage.get(City, city_id)
        if acity is None:
            abort(404)
        place_list = []
        for aplace in acity.places:
            place_list.append(aplace.to_dict())
        return jsonify(place_list), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """
    delete place if id is match with obj_place
    """
    if storage.get(Place, place_id):
        storage.delete(storage.get(Place, place_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    """
    post method to place
    """
    city = storage.get(City, city_id)
    if city:
        place_dic = request.get_json()
        if place_dic is None:
            abort(400, "Not a JSON")
        if "user_id" not in place_dic.keys():
            abort(404, "Missing user_id")
        if not storage.get("User", place["user_id"]):
            abort(404)
        if "name" not in place_dic.keys():
            abort(400, "Missing name")
        else:
            place_dic['city_id'] = city.id
            new_place = Place(**place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(place_id=None):
    """
    arreglar
    """

    data = request.get_json()

    obj = storage.get(Place, place_id)

    if obj is None:
        abort(404)

    if data is None:
        return "Not a JSON", 400

    for k, v in data.items():
        if k in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            pass
        else:
            setattr(obj, k, v)
    storage.save()

    return jsonify(obj.to_dict()), 200
