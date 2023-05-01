#!/usr/bin/python3
""" functions GET, PUT, POST & DELETE """

from flask import jsonify, request, abort,  make_response
from api.v1.views import app_views
from models.places import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_all(city_id):
    """ get all the places in cities """
    lists = []
    state = storage.get(Place, city_id)
    if state:
        for i in state.cities:
            lists.append(i.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_id(place_id):
    """ get place by id """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'])
def del_id(place_id):
    """ delete place by id """
    place = storage.get(Place, place_id)
    storage.delete(place)
    storage.save()
    if not place:
        abort(404)
    return ({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add():
    """ add place to storage """
    dct = storage.get(City, city_id)
    if not dct:
        abort(404)
    if request.json:
        content = request.get_json()
        user_id = content['user_id']
        user = storage.get(User, user_id)
        if "user_id" not in content.keys():
            return jsonify("Missing user_id"), 400
        if "name" not in content.keys():
            return jsonify("Missing user_id"), 400
        if not user:
            abort(404)
        place = Place(**content)
        setattr(place, 'city_id', city_id)
        storage.new(place)
        storage.save()
        return make_response(jsonify(place.to_dict()), 201)
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update(place_id):
    """ update places and city with id """
    dic = storage.all(Place)
    for i in dic:
        if dic[i].id == place_id:
            if request.json:
                ign = ["id", "user_id", "city_id", "created_at", "updated_at"]
                content = request.get_json()
                for items in content:
                    if items not in ign:
                        setattr(dic[i], items, content[items])
                dic[i].save()
                return jsonify(dic[i].to_dict())
            else:
                return jsonify("Not a JSON"), 400
    abort(404)


@app_views.route('/places_search', methods=['POST'])
def advanced():
    """ return all places per city, state or amenities
    return all places that has all amenities
    return all places that belong to city or state
    permited keys states, cities, amenities
    """
    # rule 0
    content = request.get_json(force=True, silent=True)
    if content is None:
        return jsonify('Not a JSON'), 400
    # rule 1
    result, places = [], []
    if len(content) == 0:
        places = storage.all("Place").values()
        for elem in places:
            result.append(elem.to_dict())
        return jsonify(result)

    flag = 0
    for key in content:
        if len(content[key]) > 0:
            flag = 1
            break
    if flag == 0:
        places = storage.all("Place").values()
        for elem in places:
            result.append(elem.to_dict())
        return jsonify(result)
    # rule 2
    if "states" in content.keys() and len(content["states"]) > 0:
        states = content["states"]
        for id in states:
            st = storage.get("State", id)
            if st:
                for city in st.cities:
                    for pl in city.places:
                        places.append(pl)
    # rule 3
    if "cities" in content.keys() and len(content["cities"]) > 0:
        cities = content["cities"]
        for id in cities:
            ct = storage.get("City", id)
            if ct:
                for pl in ct.places:
                    places.append(pl)

    places = list(set(places))

    if "amenities" in content.keys() and len(content["amenities"]) > 0:
        ame = []
        for id in content["amenities"]:
            ame.append(storage.get("Amenity", id))
        places = [pl for pl in places if all([a in pl.amenities for a in ame])]

    for elem in places:
        var = elem.to_dict()
        if "amenities" in var.keys():
            del var["amenities"]
        result.append(var)
    return jsonify(result)
