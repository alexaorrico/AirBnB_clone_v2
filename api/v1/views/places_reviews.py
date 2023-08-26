#!/usr/bin/python3
'''
Module that haldels the PLACES REVIEW RESTFull API
'''

from flask import jsonify, abort, request, Response
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_review(place_id=None):
    """
    Emphasys on all Review Objs
    """
    place = storage.get(place, place_id)
    if not place:
        abort(404)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return Response("Not a JSON", 400)
        if 'user_id' not in data:
            return Response("Missing user_id", 400)
        if 'text' not in data:
            return Response("Missing text", 400)
        user = storage.get(User, data.get('user_id'))
        if not user:
            abort(404)
        review = Review(place_id=place.id, user_id=user.id,
                        text=data.get('text'))
        review.save()
        return jsonify(review.to_dict()), 201

    all_reviews = place.reviews
    reviews = []

    for review in all_reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_review(review_id=None):
    """
    Emphasys on only on Review obj
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return Response("Not a JSON", 400)
        data['id'] = review.id
        data['user_id'] = review.user_id
        data['place_id'] = review.place_id
        data['created_at'] = review.created_at
        review.__init__(**data)
        review.save()
        return jsonify(review.to_dict()), 200

    return jsonify(review.to_dict()), 200
