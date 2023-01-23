#!/usr/bin/python3
"""Review API"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """get method for reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review)
    place_review = []
    for review in reviews.values():
        if review.place_id == place_id:
            place_review.append(review.to_dict())
    return jsonify(place_review)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Get a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create  Reviews"""
    if (storage.get(Place, place_id)) is None:
        abort(404)
    get_json = request.get_json()
    if get_json is None:
        abort(400, 'Not a JSON')
    if get_json.get('text') is None:
        abort(400, 'Missing text')
    if get_json.get('user_id') is None:
        abort(400, 'Missing user_id')
    user_id = get_json.get('user_id')
    if (storage.get(User, user_id) is None):
        abort(404)

    get_json['place_id'] = place_id
    new_review = Review(**get_json)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    update = request.get_json()

    exept = ['created_at', 'updated_at', 'id', 'user_id', 'place_id']
    for key, value in update.items():
        if key not in exept:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
