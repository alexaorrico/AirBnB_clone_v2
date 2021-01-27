#!/usr/bin/python3
"""new view for Review objects that handles all
default RestFul API actions
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route(
    "/places/<place_id>/reviews", methods=['GET'], strict_slashes=False)
def reviews_view(place_id):
    """Retrieves the list of all Review objects of a State"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)

    list_review = [value.to_dict() for value in my_place.reviews]
    return jsonify(list_review)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def review_view(review_id):
    """Retrieves a Review object"""
    my_review = storage.get(Review, review_id)
    if my_review is None:
        abort(404)
    return jsonify(my_review.to_dict())


@app_views.route(
    "/reviews/<review_id>", methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object"""
    my_review = storage.get(Review, review_id)
    if my_review is None:
        abort(404)
    storage.delete(my_review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/reviews", methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Create a new Review object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)

    content = request.get_json()
    if content is None:
        abort(400, "Not a JSON")

    user_id = content.get('user_id')
    if user_id is None:
        abort(400, "Missing user_id")

    if storage.get(User, user_id) is None:
        abort(404)

    if content.get('text') is None:
        abort(400, "Missing text")

    new_review = Review(**content)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Updates a Review object"""
    my_review = storage.get(Review, review_id)
    if my_review is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, "Not a JSON")

    keys_ignored = ['id', 'user_id', 'place_id' 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in keys_ignored:
            setattr(my_review, key, value)
    my_review.save()
    return jsonify(my_review.to_dict()), 200
