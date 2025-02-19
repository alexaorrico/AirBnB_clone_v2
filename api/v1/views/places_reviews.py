#!/usr/bin/python3
"""Review module"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False, methods=["GET"])
def get_reviews(place_id):
    """Get reviews by place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """Get review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):
    """Delete review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False, methods=["POST"])
def create_review(place_id):
    """Create review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    if 'text' not in data:
        abort(400, "Missing text")
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id):
    """Update review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
