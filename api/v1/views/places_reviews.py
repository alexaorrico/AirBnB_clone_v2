#!/usr/bin/python3
"""Defines all routes for the `review` entity
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, classes


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_reviews(place_id):
    """Returns all reviews linked to given place_id"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        return abort(404)
    reviews = place_obj.reviews
    if reviews is None:
        return abort(404)
    review_objs = []
    for review in reviews:
        review_objs.append(review.to_dict())
    return jsonify(review_objs)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """Returns review with given review_id"""
    review = storage.get("Review", review_id)
    if review is None:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route("places/<place_id>/reviews/", methods=["POST"])
def create_review(place_id):
    """Creates a new review in storage"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")
    if "text" not in data:
        return abort(400, description="Missing text")
    if "user_id" not in data:
        return abort(400, description="Missing user_id")

    place = storage.get("Place", place_id)
    user = storage.get("User", data.get("user_id"))
    if place is None or user is None:
        return abort(404)

    review = classes["Review"](**data)
    place.reviews.append(review)
    place.save()
    delattr(review, "place")
    delattr(review, "user")
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Deletes a review object from storage"""
    review = storage.get("Review", review_id)
    if review is None:
        return abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Update a review object by id"""
    review = storage.get("Review", review_id)
    if review is None:
        return abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("user_id", None)
    data.pop("place_id", None)
    data.pop("updated_at", None)
    data.pop("created_at", None)

    for k, v in data.items():
        setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict())
