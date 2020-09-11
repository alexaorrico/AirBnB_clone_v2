#!/usr/bin/python3
"""Reviews views"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews_get(place_id):
    """Retrieves the list of all Review objects os a Place"""
    all_places = storage.get('Place', place_id)
    reviews_for_json = []
    if all_places is None:
        abort(404)
    all_reviews = all_places.reviews
    for review in all_reviews:
        reviews_for_json.append(review.to_dict())
    return jsonify(reviews_for_json)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_reviews(review_id):
    """Retrieves the list of all Review objects os a Place"""
    all_review = storage.get('Review', review_id)
    if all_review is None:
        abort(404)
    else:
        return jsonify(all_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews(review_id):
    """Deletes a review"""
    to_delete = storage.get('Review', review_id)
    if to_delete is None:
        abort(404)
    storage.delete(to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_reviews():
    """Creates a REview"""
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    if "text" not in req:
        abort(400, "Missing text")
    if storage.get('User', request.json['user_id']) is None:
        abort(404)
    if storage.get('Place', place_id) is None:
        abort(404)
    new_review = Review(user_id=request.json['user_id'],
                        text=request.json['text'], place_id=place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a Review object"""
    req = request.get_json()
    review_to_modify = storage.get('Review', review_id)
    if not request.json:
        abort(400, "Not a JSON")
    if review_to_modify is None:
        abort(404)
    for key in req:
        if key not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(review_to_modify, key, req[key])
    storage.save()
    return jsonify(review_to_modify.to_dict()), 200
