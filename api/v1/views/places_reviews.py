#!/usr/bin/python3
""" Review all RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieve all reviews of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a Review"""
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if 'user_id' not in payload:
        abort(400, "Missing user_id")
    user = storage.get(User, payload['user_id'])
    if not user:
        abort(404)
    if 'text' not in payload:
        abort(400, "Missing text")
    review = Review(place_id=place_id, **payload)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    for key, value in payload.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
