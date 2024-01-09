#!/usr/bin/python3

"""Define endpoints for reviews"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def fetch_reviews(place_id):
    """Fetch reviews of a place"""
    place: Place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def fetch_review(review_id):
    """Fetch a single review by it's id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review"""
    review: Review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['DELETE'],
                 strict_slashes=False)
def add_review(place_id):
    """Add a review for a place"""
    place: Place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data = request.get_json()

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a review"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    excluded = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in excluded:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
