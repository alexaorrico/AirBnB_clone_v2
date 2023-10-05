#!/usr/bin/python3
"""A new view for Review objects that handles all default RESTFUL
API actions"""


from flask import Flask, jsonify, request, abort, redirect, url_for
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    """Retrives all Review objects in the storage
    given a place id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [r.to_dict() for r in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_based_on_id(review_id):
    """Retrives a Review object given it's id else return 404
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_object(review_id):
    """Deletes a Review object if found otherwise return 404
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review_object(place_id):
    """Creates a Review object returns the created object
    """

    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)

    data = request.get_json()
    if not data:
        # abort(400, description='Not a JSON')
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in data:
        # abort(400, description='Missing user_id')
        return jsonify({'error': 'Missing user_id'}), 400
    if 'text' not in data:
        # abort(400, description='Missing text')
        return jsonify({'error': 'Missing text'}), 400
    user_obj = storage.get(User, data['user_id'])
    if not user_obj:
        abort(404)
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review object based on the id
    """

    fetch_r = storage.get(Review, review_id)
    if not fetch_r:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    keep = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for key, values in data.items():
        if key not in keep:
            setattr(fetch_r, key, values)

    fetch_r.save()
    return jsonify(fetch_r.to_dict()), 200
