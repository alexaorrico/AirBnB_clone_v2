#!/usr/bin/python3
"""
Define route for view Review
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.city import City
from models.user import User
from models import storage


@app_views.route('/reviews/<string:review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def reviews(review_id=None):
    """Retrieves a Review or All the reviews"""
    review = storage.get(Review, review_id)

    if request.method == 'GET':
        if review_id is not None:
            if review is None:
                abort(404)
            return jsonify(review.to_dict())

    if review is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())


@app_views.route('/places/<string:place_id>/reviews',
                 strict_slashes=False, methods=['GET', 'POST'])
def review_place(place_id=None):
    """Retrieves a Review or All the reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        data = request.get_json()
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        if not data:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')

        user = storage.get(User, data.get('user_id'))
        if user is None:
            abort(404)
        if 'text' not in data:
            abort(400, 'Missing text')

        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return jsonify(review.to_dict()), 201
