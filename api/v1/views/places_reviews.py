#!/usr/bin/python3
"""
Places Reviews view
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

app = Flask(__name__)


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, "Not a JSON")
    if 'user_id' not in content:
        abort(400, "Missing user_id")
    if 'text' not in content:
        abort(400, "Missing text")
    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)
    new_review = Review(place_id=place_id, **content)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, "Not a JSON")
    for key, value in content.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
