#!/usr/bin/python3
"""
View for Reviews that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_all(place_id):
    """ returns list of all Review objects """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews_all = []
    reviews = storage.all("Review").values()
    for review in reviews:
        if review.place_id == place_id:
            reviews_all.append(review.to_json())
    return jsonify(reviews_all)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_get(review_id):
    """ handles GET method """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review = review.to_json()
    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def review_delete(review_id):
    """ handles DELETE method """
    empty_dict = {}
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """ handles POST method """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, "Missing text")
    review = Review(**data)
    review.place_id = place_id
    review.save()
    review = review.to_json()
    return jsonify(review), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_put(review_id):
    """ handles PUT method """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            review.bm_update(key, value)
    review.save()
    review = review.to_json()
    return jsonify(review), 200
