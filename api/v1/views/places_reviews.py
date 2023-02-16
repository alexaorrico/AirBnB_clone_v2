#!/usr/bin/python3

"""Review view module"""

from api.v1.views import (app_views)
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request
import models


@app_views.route('/places/<place_id>/reviews',
                 methods=["GET"], strict_slashes=False)
def reviews(place_id):
    """return all the places"""
    place = models.storage.get(Place, place_id)
    if place_id is None:
        return abort(404)
    if place is None:
        return abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def get_review_by_id(review_id=None):
    """return a by id or 404"""
    review = models.storage.get(Review, review_id)
    if review_id is None:
        return abort(404)
    if review is None:
        return abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """delete place data by id"""
    review = models.storage.get(Review, review_id)
    if review_id is None:
        return abort(404)
    if review is None:
        return abort(404)

    models.storage.delete(review)
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def add_review(place_id):
    """add new place"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        req_data = None
    if req_data is None:
        return "Not a JSON", 400
    place = models.storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if "user_id" not in req_data.keys():
        return "Missing user_id", 400
    if "text" not in req_data.keys():
        return "Missing text", 400
    user = models.storage.get(User, req_data.get("user_id"))
    if user is None:
        return abort(404)
    if "name" not in req_data.keys():
        return "Missing name", 400
    new_review = Review(**req_data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """update place object"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        return "Not a JSON", 400
    review = models.storage.get(Review, review_id)
    if review is None:
        return abort(404)
    for key in ("id", "created_at", "updated_at", "user_id", "place_id"):
        req_data.pop(key, None)
    for k, v in req_data.items():
        setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200
