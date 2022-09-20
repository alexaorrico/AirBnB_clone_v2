#!/usr/bin/python3
"""objects that handle all default RestFul API actions for Reviews"""

from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("places/<string:place_id>/reviews", strict_slashes=False)
def get_reviews(place_id):
    """Method that reviews a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("reviews/<string:review_id>", strict_slashes=False)
def one_review(review_id):
    """Method for one review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("reviews/<string:review_id>", methods=["DELETE"],
                 strict_slashes=False)
def review_delete(review_id):
    """Method that deletes a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify(({})), 200)


@app_views.route('places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """Method that creates a review"""
    place = storage.get(Place, place_id)
    data = request.get_json()
    if not place:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, description="Missing text")
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("reviews/<string:review_id>", methods=['PUT'],
                 strict_slashes=False)
def review_put(review_id):
    """Method that puts a review"""
    review = storage.get(Review, review_id)
    data = request.get_json()

    if not review:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
