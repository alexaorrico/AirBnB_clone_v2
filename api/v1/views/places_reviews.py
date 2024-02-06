#!/usr/bin/python3
"""
Define route for view Review
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.review import Review
from models.city import City
from models.user import User
from models import storage


@app_views.route('/reviews/<string:review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def reviews(review_id=None):
    """Retrieves a Review or All the reviews"""
    if request.method == 'GET':
        if review_id is not None:
            review = storage.get(Review, review_id)
            if review is None:
                abort(404)
            else:
                return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'not a json'}), 400)

        for key, value in data.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, value)
        review.save()
        return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/places/<string:place_id>/reviews',
                 strict_slashes=False, methods=['GET', 'POST'])
def review_place(place_id=None):
    """Retrieves a Review or All the reviews"""
    if request.method == 'GET':
        if place_id is not None:
            place = storage.get(Place, place_id)
            if place is None:
                abort(404)
            reviews = [review.to_dict() for review in place.reviews]
            return jsonify(reviews)

    elif request.method == 'POST':
        data = request.get_json()
        place = storage.get(Place, place_id)
        user = storage.get(User, user_id)
        if place is None:
            abort(404)
        elif not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        elif 'user_id' not in data:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        elif user is None:
            abort(404)
        elif 'text' not in data:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        else:
            review = Review(**data)
            review.save()
            return make_response(jsonify(review.to_dict()), 201)
