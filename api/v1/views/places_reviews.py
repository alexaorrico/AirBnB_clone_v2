#!/usr/bin/python3
""" A new view for Review object that handles all
    default RESTFul API actions"""

from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def review_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify([review.to_dict() for review in place.reviews])

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')
        if 'text' not in request.json:
            abort(400, 'Missing text')
        user_id = request.json['user_id']
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        new_review = Review(**request.get_json())
        new_review.place_id = place_id
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def reviews(review_id):
    """Retrieves a Review object using review_id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.json.items():
            if k not in ['id', 'user_id', 'place_id',
                         'created_at', 'updated_at']:
                setattr(review, k, v)
        review.save()
        return make_response(jsonify(review.to_dict()), 200)
