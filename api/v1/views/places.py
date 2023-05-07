#!/usr/bin/python3
""" places view """
from flask import Flask, Blueprint
from flask import abort, make_response
from flask import jsonify, request
from models import storage, city, place
from api.v1.views import app_views


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def retrieve_places():
    """ retrieve all places """
    places = []
    all_places = storage.all('Place').values()
    for place in all_places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    places = []
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    for my_place in my_city.places:
        places.append(my_place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """ Retrieves a Place object """
    a_place = storage.get('Place', place_id)
    if a_place is None:
        abort(404)
    return jsonify(a_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete a Place """
    a_place = storage.get('Place', place_id)
    if a_place is None:
        abort(404)
    storage.delete(a_place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ create a Place """
    the_city = storage.get('City', city_id)
    if the_city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    my_user = storage.get('User', request.json['user_id'])
    if my_user is None:
        abort(404)
    req = request.get_json()
    req['city_id'] = city_id
    new_place = place.Place(**req)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ update a Place """
    a_place = storage.get('Place', place_id)
    if a_place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for req in request.json:
        if req not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(a_place, req, request.json[req])
    storage.save()
    return jsonify(a_place.to_dict())


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def searchPlace():
    """ retrieves all Place objects depending on the JSON
    in the body of the request. """
    search = request.get_json()
    if search is None:
        return jsonify({"error": "Not a JSON"}), 400

    answer = set()

    if "states" in search:
        stid = [storage.get("State", stateid) for stateid in search["states"]]
        states = [st for st in stid if st is not None]
        for state in states:
            for city in state.cities:
                answer.update(set(city.places))

    if "cities" in search:
        cityid = [storage.get("City", cid) for cid in search["cities"]]
        cities = [cty for cty in cityid if cty is not None]
        for city in cities:
            for place in city.places:
                answer.add(place)

    if len(answer) == 0:
        answer = set(storage.all("Place").values())

    if "amenities" in search:
        amenities = [storage.get("Amenity", amenid)
                     for amenid in search["amenities"]]
        alist = [a for a in answer if all(amen in a.amenities
                                          for amen in amenities)]
    else:
        alist = list(answer)

    dict_plist = [pl.to_dict() for pl in alist]
    for adict in dict_plist:
        if "amenities" in adict:
            del adict["amenities"]

    return jsonify(dict_plist)
