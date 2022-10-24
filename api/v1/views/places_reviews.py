#!/usr/bin/python3

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place


@app_views.route('/api/v1/places/<string:place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_reviews(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([value.to_dict() for value in place.reviews])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400
        elif post.get('text') is None:
            return jsonify({'error': 'Missing text'}), 400
        elif storage.get('User', post.get('user_id')) is None:
            abort(404)

    new_review = Review(place_id=place_id, **post)
    new_review.save()
    return jsonify(place.to_dict()), 201


@app_views.route(' /api/v1/reviews/<string:review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_review_id(review_id):
    """Retrieves the Review object/Objects of a Place"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict()), 200

    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in put.items():
            if key not in ['id', 'created_at',
                           'updated_at', 'user_id', 'place_id']:
                setattr(review, key, value)
                storage.save()
                return jsonify(review.to_dict()), 200
