#!/usr/bin/python3
"""ALX SE Flask Api Review Module."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_place_reviews(place_id: str):
    """Return all reviews link to a particular place given its id."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_reviews(review_id: str):
    """Return a review given its id."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_review(review_id: str):
    """Delete a review from storage given its id."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['POST'], strict_slashes=False)
def create_place_review(place_id: str):
    """Create a review for a place given the place id."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        review_attrs = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'user_id' not in review_attrs:
        abort(400, 'Missing user_id')
    if 'text' not in review_attrs:
        abort(400, 'Missing text')
    user = storage.get(User, review_attrs['user_id'])
    if not user:
        abort(404)
    review = Review(**review_attrs)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>',
        methods=['PUT'], strict_slashes=False)
def update_review(review_id: str):
    """Update a review given its id."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    try:
        review_attrs = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    for attr, value in review_attrs.items():
        if attr not in (
                'id', 'user_id', 'place_id',
                'created_at', 'updated_at'):
            setattr(review, attr, value)
    review.save()
    return jsonify(review.to_dict())
