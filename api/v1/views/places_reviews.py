#!/usr/bin/python3
"""Contains all REST actions for review Objects"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.review import Review
from models import storage
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """retrieves a list of all review objects of place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    return jsonify([val.to_dict() for val in reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """retrieves a review objects"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """deletes a review objects"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def new_review(place_id):
    """creates a review objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.json:
        return make_response(jsonify({"error": "Missing text"}), 400)
    review = Review(user_id=request.get_json()['user_id'], place_id=place_id,
                    text=request.get_json()['text'])
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates a review objects"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'text' in request.json:
        review.text = request.get_json()['text']
        review.save()
    return jsonify(review.to_dict())
