#!/usr/bin/python3
"""
Create a new view for Review object that
handles all default RESTFul API actions
"""
from flask import Flask, request, jsonify, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User

app = Flask(__name__)


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list), 200


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_reviews_id(review_id):
    review = storage.get(Reviews, review_id)
    if review is None:
        return abort(404)
    else:
        return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_reviews(review_id):
    review = storage.get(Reviews, review_id)
    if review is None:
        return abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_reviews(place_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)

    user = storage.get(User, data['user_id'])
    if user is None:
        return abort(404)

    data['place_id'] = place.id
    new_review = Review(**data)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
