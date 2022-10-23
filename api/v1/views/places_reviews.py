#!/usr/bin/python3
"""This module handles review  routes"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_route(place_id):
    """
    reviews_route handles get, post request to reviews
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        reviews = list(map(lambda obj: obj.to_dict(),
                           place.reviews))
        return make_response(jsonify(reviews), 200)
    elif request.method == 'POST':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        required_info = ['user_id', 'text']
        for info in required_info:
            if info not in form_data:
                return make_response(
                    jsonify({'error': 'Missing {}'.format(info)}), 400)
        user = storage.get(User, form_data.get('user_id'))
        if user is None:
            abort(404)
        new_review = Review(place_id=place_id, **form_data)
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review_route(review_id):
    """
    review_route handles get, put, delete requests to a specific
    review

    :param  review_id: is the id of the review
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(review.to_dict()), 200)
    elif request.method == 'DELETE':
        review.delete()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        form_data = request.get_json(silent=True)
        if form_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        review.update(**form_data)
        return make_response(jsonify(review.to_dict()), 200)
