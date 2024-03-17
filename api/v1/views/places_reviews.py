#!/usr/bin/python3
""" retruns json response status of API """
from flask import Flask, abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    ''' gets the list of all City objects of a State '''
    place_id = storage.get(Place, place_id)
    if place_id is None:
        abort(404)
    reviews_list = [review.to_dict() for review in place_id.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    ''' gets specific state objects by its state ID '''
    review_object = storage.get(Review, review_id)
    if review_object is None:
        abort(404)
    return jsonify(review_object.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    ''' deletes review object '''
    review_object = storage.get(Review, review_id)
    if review_object is None:
        abort(404)
    storage.delete(review_object)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    '''' creates a review '''
    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404)
    response = request.get_json(silent=True)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in response:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in response:
        return make_response(jsonify({'error': 'Missing text'}), 400)

    user_id = storage.get(User, response['user_id'])
    if user_id is None:
        abort(404)

    new_review = Review(**response)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''' updates a city object '''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    response = request.get_json(silent=True)
    if response is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in response.items():
        if key not in ['id', 'place_id', 'user_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(review.to_dict(), 200)
