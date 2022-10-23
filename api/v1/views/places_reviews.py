#!/usr/bin/python3
"""route for reviews"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models import storage
from flask import abort, jsonify, request, make_response


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def get_place_review(place_id):
    """retrieves the list of all Review objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    all_place_reviews = []
    for review in place.reviews:
        all_place_reviews.append(review.to_dict())
    return jsonify(all_place_reviews)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET"])
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())
