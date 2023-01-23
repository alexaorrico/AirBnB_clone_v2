#!/usr/bin/python3
""" Lists reviews """

from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id=None):
    """
    Returns list of review objects linked to any place
    with place_id: Returns review objects
    without place_id: 404
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['GET'])
def get_review_id(review_id):
    '''
    Get review by review id
    '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id=None):
    """
    Deletes a review from the database
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_review(place_id=None):
    """
    Post a review
    """
    req = request.get_json()
    if storage.get(Place, place_id) is None:
        abort(404)
    if not req:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    if storage.get(User, req["user_id"]) is None:
        abort(404)
    if "text" not in req:
        abort(400, "Missing text")

    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id=None):
    """ Update a state object
    """
    key = "Review." + str(review_id)
    if key not in storage.all(Review).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    review = storage.get(Review, review_id)
    for key, value in request.get_json().items():
        if key not in ["created_at", "updated_at", "id"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
