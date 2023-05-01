#!/usr/bin/python3
""" place review apply REST"""

from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def rev(place_id):
    """ list of objetc to review """
    new = []
    dic = storage.all('Place')
    for i in dic:
        if dic[i].id == place_id:
            var = dic[i].reviews
            for j in var:
                new.append(j.to_dict())
            return jsonify(new)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def rev_id(review_id):
    """ review with id """
    dic = storage.all('Review')
    for i in dic:
        if dic[i].id == review_id:
            return jsonify(dic[i].to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def rev_delete(review_id):
    """ delete a review """
    dic = storage.all('Review')
    for key in dic:
        if review_id == dic[key].id:
            dic[key].delete()
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_rev(place_id):
    """ create a review of a specified city
    """
    new = []
    obj = storage.get("Place", place_id)
    content = request.get_json()
    if not obj:
        abort(404)
    if not request.json:
        return jsonify("Not a JSON"), 400
    else:
        if "user_id" not in content.keys():
            return (jsonify("Missing user_id"), 400)
        obj2 = storage.get("User", content["user_id"])
        if not obj2:
            abort(404)
        if "text" not in content.keys():
            return jsonify("Missing text"), 400

        content["place_id"] = place_id
        new_place = Review(**content)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_rev(review_id):
    """ update a specified place """
    dic = storage.all('Review')
    for key in dic:
        if review_id == dic[key].id:
            if not request.json:
                return (jsonify("Not a JSON"), 400)
            else:
                ignore = ["id", "updated_at", "created_at",
                          "place_id", "user_id"]
                content = request.get_json()
                for k in content:
                    if k not in ignore:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return jsonify(dic[key].to_dict())
    abort(404)
