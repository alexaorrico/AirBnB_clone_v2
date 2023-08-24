#!/usr/bin/python3
"""places views"""
from models.review import Review
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def retrives_all_review(place_id):
    """Retrives the list of all reviews"""
    if storage.get(Place, place_id) is None:
        abort(404)
    place = storage.get(Place, place_id)
    return jsonify([
        reviews.to_dict() for reviews in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'])
def retrives_review(review_id):
    """Retrives a review from id"""
    if storage.get(Review, review_id) is None:
        abort(404)
    return jsonify(storage.get(Review, review_id).to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """creates a new review"""
    if storage.get(Place, place_id) is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_data:
        abort(400, 'Missing user_id')
    if 'text' not in json_data:
        abort(400, 'Missing text')
    review = Review(**json_data)
    if storage.get(User, review.user_id) is None:
        abort(404)
    setattr(review, 'place_id', place_id)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """update a review"""
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    review = storage.get(Place, review_id)
    if review is None:
        abort(404)
    for key, values in json_data.items():
        if key not in ('id', 'created_at', 'updated_at', 'place_id', 'user_id'):
            setattr(review, key, values)
    review.save()
    return jsonify(review.to_dict()), 200
