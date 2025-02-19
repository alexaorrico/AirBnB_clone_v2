#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews")
def get_reviews(place_id):
    """get all reviews"""
    res = storage.get(Place, place_id)
    if res is None:
        abort(404)
    else:
        reviews = []
        for review in res.reviews:
            reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>")
def get_review(review_id):
    """get review"""
    res = storage.get(Review, review_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """delete review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """add new review"""
    if request.json is None:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data.get('user_id') is None:
        return "Missing user_id", 400
    user = storage.get(User, data.get('user_id'))
    if user is None:
        abort(404)
    if data.get('text') is None:
        return "Missing text", 400
    new_review = Review(text=request.json['text'])
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """update review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if request.json is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
