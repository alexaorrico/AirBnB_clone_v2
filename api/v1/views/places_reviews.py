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
    if Review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if "user_id" not in data:
        abort(400, 'Missing user_id')
    if "text" not in data:
        abort(400, 'Missing text')

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if User is None:
        abort(404)

    data['place_id'] = place.id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()

    return jsonify(review.to_dict()), 201


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
            setattr(review, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
