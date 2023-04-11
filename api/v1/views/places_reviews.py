#!/usr/bin/python3
"""Reviews API routes"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Place Reviews objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object"""
    place = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    if 'user_id' not in req_json:
        abort(400, "Missing user_id")
    user = storage.get(User, req_json['user_id'])
    if user is None:
        abort(404)
    if 'text' not in req_json:
        abort(400, "Missing text")
    req_json['place_id'] = place_id
    review = Review(**req_json)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
    '/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    ignore_key = ['id', 'user_id', 'place_id' 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore_key:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
