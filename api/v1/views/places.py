#!/usr/bin/python3
""" functions GET, PUT, POST & DELETE """

from flask import jsonify, request, abort,  make_response
from api.v1.views import app_views
from models.places import Place
from models.city import City
from models import storage


@app_views.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_all(city_id):
    """ get all the places in cities """
    lists = []
    state = storage.get(Place, city_id)
    if state:
        for i in state.cities:
            lists.append(i.to_dict())
    abort(404)


@app_views.route('/api/v1/places/<place_id>', methods=['GET'])
def get_id(place_id):
    """ get place by id """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route("/api/v1/places/<place_id>", methods=['DELETE'])
def del_id(place_id):
    """ delete place by id """
    place = storage.get(Place, place_id)
    storage.delete(place)
    storage.save()
    if not place:
        abort(404)
    return ({}), 200


@app_views.route('/api/v1/cities/<city_id>/places', methods=['POST'])
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


@app_views.route('/api/v1/places/<place_id>', methods=['PUT'])
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
