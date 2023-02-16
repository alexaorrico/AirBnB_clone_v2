#!/usr/bin/python3
""" Place_reviews APIRest
"""

from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def rev_list(place_id):
    """ list of objetc in dict form
    """
    lista = []
    dic = storage.all('Place')
    for elem in dic:
        if dic[elem].id == place_id:
            var = dic[elem].reviews
            for i in var:
                lista.append(i.to_dict())
            return (jsonify(lista))
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review(review_id):
    """ list of objetc in dict form
    """
    dic = storage.all('Review')
    for elem in dic:
        if dic[elem].id == review_id:
            return (jsonify(dic[elem].to_dict()))
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def rev_delete(review_id):
    """ delete the delete
    """
    dic = storage.all('Review')
    for key in dic:
        if review_id == dic[key].id:
            dic[key].delete()
            storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_rev(place_id):
    """ create a review of a specified city
    """
    lista = []
    obj = storage.get("Place", place_id)
    content = request.get_json()
    if not obj:
        abort(404)
    if not request.json:
        return (jsonify("Not a JSON"), 400)
    else:
        if "user_id" not in content.keys():
            return (jsonify("Missing user_id"), 400)
        obj2 = storage.get("User", content["user_id"])
        if not obj2:
            abort(404)
        if "text" not in content.keys():
            return (jsonify("Missing text"), 400)

        content["place_id"] = place_id
        new_place = Review(**content)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_rev(review_id):
    """ update a specified place
    """
    dic = storage.all('Review')
    for key in dic:
        if review_id == dic[key].id:
            if not request.json:
                return (jsonify("Not a JSON"), 400)
            else:
                forbidden = ["id", "update_at", "created_at",
                             "place_id", "user_id"]
                content = request.get_json()
                for k in content:
                    if k not in forbidden:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return jsonify(dic[key].to_dict())
    abort(404)
