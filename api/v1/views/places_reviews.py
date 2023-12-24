#!/usr/bin/python3
"""create a new view for Review that handles all default RESTFul API actions"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
import json
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_all_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for k in place.reviews:
        reviews_list.append(k.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, 'Place not found')

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404, 'User not found')
    if 'text' not in data:
        abort(400, 'Missing text')

    data['place_id'] = place.id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, value in data.items():
        if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, k, value)
    storage.save()
    return jsonify(review.to_dict()), 200
