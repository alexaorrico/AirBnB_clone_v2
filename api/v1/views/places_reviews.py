#!/usr/bin/python3
"""Reviews view """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', method=['GET'])
def all_reviews(place_id):
    """Returns a list of reviews"""
    if not storage.get("Place", place_id):
        abort(404)

    reviews = []

    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>')
def get_method_place(review_id):
    """Returns a review from id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def del_method_review(review_id):
    """deletes a review"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)
    storage.delete()
    storage.save()
    return jsonify({})


@app_views.route('/placess/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """creates a review"""
    if not storage.get("place", place_id):
        abort(404)

    if not request.get_json():
        return make_reponse(jsonify({'error': "Not a JSON"}), 400)

    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_reponse(jsonify({'error': "Missing user_id"}), 400)

    user = storage.get("User", kwargs['user_id'])
    if user is None:
        abort(404)

    if 'text' not in kwargs:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """updates review module"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(place, key, value)

    review.save()
    return jsonify(review.to_dict())
