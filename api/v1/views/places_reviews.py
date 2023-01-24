#!/usr/bin/python3
"""Place_review view"""

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews_for_a_place(place_id=None):
    """
    get a review that is associated to a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    new_list = []
    for review in place.reviews:
        new_list.append(review.to_dict())
    return jsonify(new_list)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review(review_id=None):
    """
    retrieve one review
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """
    delete a review that the id was passed
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id=None):
    """
    create a review for a place
    by using the place_id to select the place
    """
    if storage.get(Place, place_id) is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    if storage.get(Place, request.get_json()["user_id"]) is None:
        abort(404)
    if "text" not in request.get_json():
        abort(400, "Missing text")

    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id=None):
    """
    update a review
    by passing th review_id
    """
    key = "Review." + str(review_id)
    if key not in storage.all(Review).keys():
        abort(404)
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "update_at",
                       "user_id", "place_id"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
