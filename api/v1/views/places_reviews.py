#!/usr/bin/python3
"""Module to create a new view for Review objects"""
from flask import jsonify, Flask, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """Retrieves the list of all Review objs of a Place by place_id"""
    place = storage.get('Place', place_id)
    list_of_reviews = []
    if place is None:
        abort(404)
    for review in place.reviews:
        list_of_reviews.append(review.to_dict())
    return jsonify(list_of_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_review_id(review_id):
    """Retrieves a Review object by review_id"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """Deletes a review by ID"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Post a Review object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400)
        abort(Response("Not a JSON"))

    if 'text' not in data:
        abort(400)
        abort(Response("Missing text"))

    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Put a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in data.items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(review, k, v)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 200
