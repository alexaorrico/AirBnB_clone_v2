#!/usr/bin/python3
"""State view module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """gets the list of all reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = [r.to_dict() for r in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def review_from_id(review_id):
    """retrieves review object by
    its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(place_id):
    """deletes a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review():
    """creates a review object"""
    data = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'text' not in data:
        abort(400, 'Missing text')
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
