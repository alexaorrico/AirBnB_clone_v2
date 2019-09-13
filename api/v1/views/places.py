#!/usr/bin/python3
""" API REST for City """
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request
from os import getenv


def check_amenities(place):
    """ helper function """
    place_dict = place.to_dict()
    if "amenities" in place_dict:
        del place_dict["amenities"]
    return place_dict


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
    if storage.get("City", city_id) is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        if 'user_id' not in data:
            return jsonify(error="Missing user_id"), 400
        if storage.get("User", data["user_id"]) is None:
            abort(404)
        if 'name' not in data:
            return jsonify(error="Missing name"), 400
        data["city_id"] = city_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    else:
        return jsonify(error="Not a JSON"), 400


@app_views.route('/places_search', methods=['POST'])
def create_search():
    """ Route search places based on JSON """
    amenities_l = []
    cities_l = []
    places_l = []
    if request.is_json:
        data = request.get_json()
        if len(data) is 0:
            places_l = storage.all('Place')
        else:
            if 'states'in data and len(data["states"]) is not 0:
                for my_states in data["states"]:
                    cities_l += storage.get('State', my_states).cities
            if 'cities' in data and len(data["cities"]) is not 0:
                cities_l.append(data["cities"])
                for my_cities in cities_l:
                    places_l += list(map(lambda x: x.places,
                                         storage.get('City', my_cities)))
            if 'amenities' in data and len(data["amenities"]) is not 0:
                if getenv("HBNB_TYPE_STORAGE") == 'db':
                    places_l += list(filter(lambda x:
                                            all(elem in
                                                list(map(lambda y: y.id,
                                                         x.amenities))
                                                for elem in data["amenities"]),
                                            storage.all('Place').values()))
                else:
                    places_l += list(filter(lambda x: all(elem in x.amenity_ids
                                            for elem in data["amenities"]),
                                            storage.all('Place').values()
            if len(places_l) is 0:
                places_l = storage.all('Place').values()
            return jsonify(list(map(check_amenities, places_l))), 200
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
                                "user_id", "city_id"]:
                    setattr(my_object, keys, values)
            my_object.save()
            return jsonify(my_object.to_dict()), 200
        else:
            abort(404)
    else:
        return jsonify(error="Not a JSON"), 400
