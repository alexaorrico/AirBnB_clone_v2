#!/usr/bin/python3
""" Reviews """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views, storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def list_reviews(place_id):
    """List all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by review_id"""
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by review_id"""
    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object in a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_dict = request.get_json(silent=True)
    if request_dict is not None:
        if 'user_id' not in request_dict or request_dict['user_id'] is None:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        user = storage.get(User, request_dict['user_id'])
        if user is None:
            abort(404)
        if 'text' not in request_dict.keys() or request_dict['text'] is None:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        new_review = Review(**request_dict)
        new_review.place_id = place_id
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)
    return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by review_id"""
    request_dict = request.get_json(silent=True)
    data = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    if request_dict is not None:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        for key, val in request_dict.items():
            if key not in data:
                setattr(review, key, val)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
