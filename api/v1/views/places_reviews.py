#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """Retrieve the list of all Review objects of a City"""
    review_l = []
    place_o = storage.get(Place, place_id)
    if not place_o:
        abort(404)
    for obj in place_o.reviews:
        review_l.append(obj.to_json())

    return jsonify(review_l)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a review object"""
    rev_iew = storage.get(Review, review_id)
    if not rev_iew:
        abort(404)
    return jsonify(rev_iew.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review object"""
    rev_iew = storage.get(Review, review_id)
    if not rev_iew:
        abort(404)
    storage.delete(rev_iew)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a Review"""
    
    rev_iew = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    user = storage.get(User, request.json['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.json:
        abort(400, description="Missing name")

    rev_iew['place_id'] = place_id
    new_review = Review(**rev_iew)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    rev_iew = storage.get(Review, review_id)
    if not rev_iew:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")

    rev_iew_j = request.get_json()
    ignore_keys = {'id', 'user_id', 'city_id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(rev_iew, key, value)
    rev_iew.save()
    return jsonify(rev_iew.to_dict()), 200
