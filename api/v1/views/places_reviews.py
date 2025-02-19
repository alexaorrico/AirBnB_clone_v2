#!/usr/bin/python3
"""
Module that creates a new view for Review object that handles
all default RESTFul API actions
"""

from models.user import User
from models.review import Review
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def review_all(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_by_id(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    newReview = request.get_json()
    user = storage.get(User, newReview['user_id'])
    if user is None:
        return abort(404)
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    newReview['place_id'] = place_id
    instance = Review(**newReview)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    request_dict = request.get_json()
    for key, val in request_dict.items():
        if key not in ["id", "created_at", "updated_at",
                       "place_id", "user_id"]:
            setattr(review, key, val)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
