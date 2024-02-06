#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review
from api.vi.views import app_views


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    """Retreive the list of all reviews objects"""
    reviews = storage.all(Review).values()
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slasheds=False)
def get_review(review_id):
    """Retrieve the specific review object by Id"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slasheds=False)
def delete_review(review_id):
    """Delete a Review object by ID"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/reviews', methods=['POST'], strict_slasheds=False)
def create_review():
    """Create a new review object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slasheds=False)
def update_review(review_id):
    """Update a Review Object by ID"""
    if review:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a Json"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(review, key, value)


        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
