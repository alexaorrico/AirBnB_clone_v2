#!/usr/bin/python3
""" View Review """

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review


@app_views.route("/places/<id>/reviews", methods=["GET"])
def reviewAll(id):
    """id places retrieve json object with his reviews"""
    ll = []
    s = storage.all('Place').values()
    ss = storage.all('Review').values()
    for v in s:
        if v.id == id:
            for vv in ss:
                if vv.place_id == id:
                    ll.append(vv.to_dict())
    if not ll:
        return abort(404)
    return jsonify(ll)


@app_views.route("/reviews/<id>", methods=["GET"])
def reviewId(id):
    """id review retrieve json object"""
    ll = []
    s = storage.all('Review').values()
    for v in s:
        if v.id == id:
            ll.append(v.to_dict())
    if not ll:
        return abort(404)
    return jsonify(ll)


@app_views.route("/reviews/<id>", methods=["DELETE"])
def reviewDel(id):
    """delete review with id"""
    review = storage.get("Review", id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<id>/reviews', methods=['POST'])
def reviewPost(id):
    """ POST a new review"""
    if storage.get("Place", id) is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    x = request.get_json()
    if "User." + x["user_id"] not in storage.all("User"):
        abort(404)
    x['place_id'] = str(id)
    if "user_id" not in x:
        return jsonify({"error": "Missing user_id"}), 400
    if "text" not in x:
        return jsonify({"error": "Missing text"}), 400
    s = Review(**x)
    s.save()
    return jsonify(s.to_dict()), 201


@app_views.route('/reviews/<id>', methods=['PUT'])
def reviewPut(id):
    """ Update a review object """
    ignore = {"id", "user_id", "place_id", "created_at", "updated_at"}
    review = storage.get("Review", id)
    if review is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    x = request.get_json()
    for k, v in x.items():
        if k not in ignore:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200
