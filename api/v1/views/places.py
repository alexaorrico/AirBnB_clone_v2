#!/usr/bin/python3
""" API REST for City """
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places')
def places_all(city_id):
    """ Route return all places in cities referenced id """
    my_city = storage.get('City', city_id)
    try:
        return jsonify(list(map(lambda x: x.to_dict(), my_city.places)))
    except:
        abort(404)


@app_views.route('/places/<place_id>')
def places_id(place_id):
    """ Route return place with referenced id """
    my_place = storage.get('Place', place_id)
    try:
        return jsonify(my_place.to_dict())
    except:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_id(place_id):
    """ Route delete place with referenced id """
    my_object = storage.get('Place', place_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_places(city_id):
    """ Route create place with POST"""
    if request.is_json:
        data = request.get_json()
        if not storage.get("City", city_id):
            abort(404)
        if 'name' not in data:
            return jsonify(error="Missing name"), 400
        if 'user_id' not in data:
            return jsonify(error="Missing user_id"), 400
        data["state_id"] = state_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    else:
        return jsonify(error="Not a JSON"), 400


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_places(place_id):
    """ Route update places with PUT """

    if request.is_json:
        data = request.get_json()
        my_object = storage.get('Place', place_id)
        if my_object is not None:
            for keys, values in data.items():
                if keys not in ["created_at", "updated_at", "id",
                                "place_id", "city_id"]:
                    setattr(my_object, keys, values)
            my_object.save()
            return jsonify(my_object.to_dict()), 200
        else:
            abort(404)
    else:
        return jsonify(error="Not a JSON"), 400
