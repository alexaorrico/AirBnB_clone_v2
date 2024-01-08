#!/usr/bin/python3
"""
handles all default RESTFul API actions for review objects
"""
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                    strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get("Place", place_id)
    if place:
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                    strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                    strict_slashes=False)
def create_review(place_id):
    """ Creates a Review """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    user = storage.get("User", request.get_json()["user_id"])
    if not user:
        abort(404)
    if "text" not in request.get_json():
        abort(400, "Missing text")
    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
