#!/usr/bin/python3
"""
Defines Review endpoints
"""
from models import storage
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def get_all_reviews(place_id):
    """Gets all Reviews by Place id."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    """Gets a Review by id."""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return review.to_dict()


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_reviews(review_id):
    """Deletes a Review."""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def post_reviews(place_id):
    """Creates an Review."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    if "user_id" not in json_data:
        return "Missing user_id", 400
    user = storage.get("User", json_data["user_id"])
    if user is None:
        abort(404)
    if "text" not in json_data:
        return "Missing text", 400
    json_data["place_id"] = place_id
    new_review = Review(**json_data)
    new_review.save()
    return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Updates an Review."""
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    for key, value in json_data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return review.to_dict(), 200
