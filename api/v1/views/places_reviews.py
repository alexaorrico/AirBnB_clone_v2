#!/usr/bin/python3
"""
New view for Review object that handles all default RESTFul API actions
"""

from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage, Place, Review, User

# Route to retrieve a list of all Review objects of a Place
@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

# Route to retrieve a specific Review object by review_id
@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

# Route to delete a specific Review object by review_id
@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

# Route to create a new Review object
@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, description="Missing text")
    
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    
    return jsonify(new_review.to_dict()), 201

# Route to update a specific Review object by review_id
@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    
    # Ignore keys: id, user_id, place_id, created_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    
    review.save()
    
    return jsonify(review.to_dict()), 200
