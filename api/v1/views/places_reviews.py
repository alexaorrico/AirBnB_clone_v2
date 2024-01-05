#!/usr/bin/python3
"""view for places_reviews.py objects handles all
   default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def place_reviews(place_id):
    """Retrieves the list of all review objects of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = []
    for review in place.reviews:
        data.append(review.to_dict())
    return jsonify(data)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves review info/object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def new_review(place_id):
    """create a new review"""
    data = request.get_json()
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    data['place_id'] = place_id
    review = Review(**data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """update review object"""
    data = request.get_json()
    review = storage.get(Review, review_id)
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if review is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
