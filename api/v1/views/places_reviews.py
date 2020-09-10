#!/usr/bin/python3
"""Reviews Api Module"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews_id(place_id):
    """Return all Review objects through the HTTP GET request."""
    if storage.get(Place, place_id) is None:
        abort(404)
    all_reviews = storage.all(Review).values()
    specific_reviews = []
    for review in all_reviews:
        if review.place_id == place_id:
            specific_reviews.append(review.to_dict())
    return jsonify(specific_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviews_id_get(review_id):
    """Get a specific Review object through the HTTP GET request."""
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    return jsonify(obj_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviews_id_delete(review_id):
    """Delete a specific Review object through the HTTP DELETE request."""
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    storage.delete(obj_review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def reviews_push(place_id):
    """Create a new Reviews object through the HTTP POST request"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if not request.get_json(silent=True):
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "user_id" not in req:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if storage.get(User, req['user_id']) is None:
        abort(404)
    if "text" not in req:
        return make_response(jsonify({"error": "Missing text"}), 400)
    req['place_id'] = place_id
    review = Review(**req)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def reviews_id_put(review_id):
    """Update a specific Review object through the HTTP PUT request."""
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    if not request.get_json(silent=True):
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    for key, value in req.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(obj_review, key, value)
    obj_review.save()
    return make_response(jsonify(obj_review.to_dict()), 200)
