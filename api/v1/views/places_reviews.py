#!/usr/bin/python3
"""script that starts a Flask web application"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review

app = Flask(__name__)


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id=None):
    """Retrieves the list of all Reviews for a place"""
    places = storage.all('Place')
    place = places.get('Place' + '.' + place_id)
    if place is None:
        abort(404)
    reviews_list = []
    reviews = storage.all('Review')
    for review in reviews.values():
        if review.place_id == place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list), 200


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id=None):
    """Retrieves a Review object with the id linked to it"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id=None):
    """Deletes a Review object"""
    obj = storage.get('Review', review_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    """Creates a review"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    result = request.get_json()
    if result is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in result:
        return jsonify({"error": "Missing user_id"}), 400
    user_obj = storage.get('User', result['user_id'])
    if user_obj is None:
        abort(404)
    if 'text' not in result:
        return jsonify({"error": "Missing text"}), 400
    review_obj = Review(place_id=place_id)
    for key, value in result.items():
        setattr(review_obj, key, value)
    storage.new(review_obj)
    storage.save()
    return jsonify(review_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """Updates a Review object"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    result = request.get_json()
    if result is None:
        return jsonify({"error": "Not a JSON"}), 400
    invalid_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in result.items():
        if key not in invalid_keys:
            setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict()), 200
