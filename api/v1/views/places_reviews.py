#!/usr/bin/python3
"""
Rest api for Reviews
"""
from models.base_model import BaseModel, Base
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_review(place_id=None):
    """ Show all review objects """
    lista = []
    flag = 0
    for v in storage.all(Place).values():
        if v.id == place_id:
            for place in v.reviews:
                lista.append(place.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(lista))


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def onereview(review_id=None):
    """ Show the review object """
    flag = 0
    for v in storage.all(Review).values():
        if v.id == review_id:
            attr = (v.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(attr))


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_reviews(review_id=None):
    """ delete """
    dicti = {}
    flag = 0
    for v in storage.all(Review).values():
        if v.id == review_id:
            storage.delete(v)
            storage.save()
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(dicti), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_reviews(place_id=None):
    """ Post and create object """
    if not request.json:
        abort(400, "Not a JSON")
    if 'text' not in request.json:
        abort(400, "Missing text")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    result = request.get_json()
    obj = Review()
    flag = 0
    for v in storage.all(Place).values():
        if v.id == place_id:
            for user in storage.all(User).values():
                if result["user_id"] == user.id:
                    for k, values in result.items():
                        flag += 1
                        setattr(obj, k, values)
                        if flag == 1:
                            setattr(obj, "place_id", place_id)
                            flag += 1
                    storage.new(obj)
                    storage.save()
                    var = obj.to_dict()
    if flag == 0:
        abort(404)
    else:
        return (jsonify(var), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def change_Reviews(review_id=None):
    """ change an class atribute """
    lista = ["user_id", "id", "place_id", "created_at", "updated_at"]
    if not request.json:
        abort(400, "Not a JSON")
    for security in lista:
        if security in request.json:
            abort(400)

    result = request.get_json()
    flag = 0
    for values in storage.all(Review).values():
        if values.id == review_id:
            for k, v in result.items():
                setattr(values, k, v)
                storage.save()
                attr = (values.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(attr), 200)
