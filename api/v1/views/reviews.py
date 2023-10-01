#!/usr/bin/python3
"""
Review model hold the endpoint (route) and their respective view functions
"""
from api.v1.views import (app_views, Review, storage)
from flask import (abort, jsonify, request)


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def all_reviews(place_id):
    """Example endpoint returning a list of all reviews
    Retrieves a list of all reviews associated with a place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_json() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def one_review(review_id):
    """Example endpoint returning a list of one reivew
    Retrieves a list of one review associated with a place
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_json())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_one_review(review_id):
    """Example endpoint deleting one review
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Example endpoint creates one review
    Creates one review associated with a place_id
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if "user_id" not in r.keys():
        return "Missing user_id", 400
    if "text" not in r.keys():
        return "Missing text", 400
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    user = storage.get("User", r["user_id"])
    if user is None:
        abort(404)
    review = Review(**r)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_json()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Example endpoint creates one review
    Creates one review associated with a place_id
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    for k in ("id", "user_id", "place_id", "created_at", "updated_at"):
        r.pop(k, None)
    for key, value in r.items():
        setattr(review, key, value)
    review.save()
    return jsonify(review.to_json()), 200
